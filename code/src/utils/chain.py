import os,os.path
import json
import traceback
import re
from app.db import AzureBlobStorage
import ast

class chain:
    def __init__(self, azure_blob_service: AzureBlobStorage(), blob_keys):
        self.azure = azure_blob_service
        self.blob_keys = blob_keys
   

    def get_filelist(self, dir, filelist):
        if os.path.isfile(dir):
            if dir.endswith('.py'):
                filelist.append(dir) 
            else:
                os.remove(dir)  
        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                new_dir = os.path.join(dir, s)
                self.get_filelist(new_dir, filelist)

        return filelist

    
    def FindImport(self,File,Filelist,object,syspath):

        
        current_dir = os.path.dirname(File)

        module_parts = object.split('.')

        rela_path = current_dir 

        abs_path = "" 
        flag = 0
        
        for i,part in enumerate(module_parts):
            if part == '':
                if flag == 0:
                    flag = 1
                elif flag == 1:    
                    rela_path = os.path.dirname(rela_path)   
            else:
                abs_path = abs_path + '/' + part

                
        
        exsitfile = []
        if syspath:   
            for path in syspath:
                exsitfile=self.get_filelist(path,exsitfile)
            parts = abs_path.split('/')[1:]

            for i in range(len(parts), 0, -1):
                new_path = '/' + '/'.join(parts[:i])
                for file in exsitfile:
                    if file.endswith(new_path + '.py'):
                        return file
                    elif file.endswith(new_path + '/__init__.py'):
                        return file
                    else:
                        continue
            exsitfile = []

        elif flag == 1:  
            exsitfile = [file for file in Filelist if os.path.dirname(file) == rela_path]
            parts = abs_path.split('/')[1:]
            for i in range(len(parts), 0, -1):
                new_path = '/' + '/'.join(parts[:i])
                for file in exsitfile:
                    if file.endswith(new_path + '.py'):
                        return file
                    elif file.endswith(new_path + '/__init__.py'):
                        return file
                    else:
                        continue

        else:
            parts = abs_path.split('/')[1:]
            new_paths = []
            for i in range(len(parts), 0, -1):
                new_path = '/' + '/'.join(parts[:i])
                for file in Filelist:
                    if file.endswith(new_path + '.py'):
                        return file
                    elif file.endswith(new_path + '/__init__.py'):
                        return file
                    else:
                        continue

        return None
        

    def remove_alias(self,import_statement):
        sentences = import_statement.split(' as ')
        modules = import_statement.split(' as ')[0]
        if len(sentences) > 1:
            alias =  import_statement.split(' as ')[1].split(',')
            return modules,alias
        else:
            return modules,''


    def extract_text_in_parentheses(self,text):
        pattern = r"\(\d+,\s*'([^']*)'\)"
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
        else:
            return ''
            
    def get_imports(self, line, syspath):
        try:
            line = line.split('#')[0] 
            sysalias = ['sys'] 


            sysaliaspath = [f'{alias}.path' for alias in sysalias]
            for item in sysaliaspath:
                if item in line:
                    syspath.append(self.extract_text_in_parentheses(line))


            if line.startswith('import'):
                line, alias = self.remove_alias(line)
                line_parts = line.replace('import', '').replace(' ', '').split(',')
                if 'sys' in line:
                    alias_parts = alias.split(',')
                    for i, module in enumerate(line_parts):
                        if module.strip() == 'sys' and i < len(alias_parts):
                            sysalias.append(alias_parts[i].strip())
                return line_parts


            elif line.startswith('from'):
                if 'import' in line:
                    parts = line.split('import', 1)
                    if len(parts) == 2:
                        module_part, functions_part = parts
                        module_part, alias = self.remove_alias(module_part.strip())
                        function_names = functions_part.split(',')
                        return [f'{module_part}.{function.strip()}' for function in function_names]
                return None

            return None
        except Exception as e:

            print(f"Error processing import line: {line}, Error: {e}")
            return None



    def GeneraterawGraph(self):
        graph = {}
        for file_key in self.blob_keys:
            graph[file_key] = []
            file_content = self.azure.download_blob(file_key).decode('utf-8')
            syspath=[]
            sysModule = []
            code = file_content
            try:
                parsed_code = ast.parse(code)
                for node in ast.walk(parsed_code):
                    if isinstance(node, ast.stmt):
                        lines = ast.unparse(node)

                        imports = self.get_imports(lines,syspath)
                        if imports is not None:
                            for i in imports:
                                item = self.FindImport(file_key, self.blob_keys, i,syspath)
                                if item is not None:
                                    if item not in sysModule:
                                        sysModule.append(item)
                                        graph[file_key].append(item)
            except SyntaxError as e:
                pass
          
        return graph
    
    def convert_to_children_representation(self, graph):
        children_representation = {}
        for node, parents in graph.items():
            if node not in children_representation:
                children_representation[node] = []
            for parent in parents:
                if parent not in children_representation:
                    children_representation[parent] = []
                children_representation[parent].append(node)
        return children_representation      


    def generate(self, repo_name):
        try:
            rawGraph = self.GeneraterawGraph()
            graph = self.convert_to_children_representation(rawGraph)
            graph_json = json.dumps(graph)
            graph_key = self.azure.save(f'code_chain/{repo_name}_dependency_graph.json', graph_json, 'dependency_graphs')
            return graph_key
        except Exception as e:
            traceback.print_exc()
            return None