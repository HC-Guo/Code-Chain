import os
import json
from bson import json_util 

from app.db import MongoDB, AzureBlobStorage
from app.config import Settings



def download_repos_data():
    settings = Settings()
    mongodb = MongoDB()
    azure_storage = AzureBlobStorage()
    collection = mongodb.db[settings.mongo_collection_name]

    # 创建一个用于保存数据的目录
    base_dir = "downloaded_repos"
    os.makedirs(base_dir, exist_ok=True)

    # 查询 MongoDB 中的文档
    pipeline = [
        {
            "$match": {
                'file_keys': { '$type': 'array' },  # 确保 file_keys 字段是数组类型
                "$expr": {
                    "$gte": [{ "$size": "$file_keys" }, 5]
                }
            }
        },
        {"$sample": {"size": 1}},
    ]
    documents = collection.aggregate(pipeline)




    for doc in documents:
        # 将文档中的 ObjectId 转换为字符串
        doc = json.loads(json_util.dumps(doc))

        # 保存文档信息
        repo_name = doc['repo_info']['name']
        doc_path = os.path.join(base_dir, f"{repo_name}.json")
        with open(doc_path, 'w') as file:
            json.dump(doc, file, indent=4)

        # 下载所有相关的 Blob 文件
        blob_keys = doc.get('file_keys', []) + [doc.get('graph_key')]
        for blob_key in blob_keys:
            if blob_key:  # 确保 blob_key 非空
                file_content = azure_storage.download_blob(blob_key)
                file_path = os.path.join(base_dir, blob_key)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as file:
                    file.write(file_content)

if __name__ == "__main__":
    download_repos_data()
