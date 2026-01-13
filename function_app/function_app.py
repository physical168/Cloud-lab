import azure.functions as func
import azure.durable_functions as df
import logging
import urllib.request
import re
from collections import Counter

# 声明这是一个 Durable Function App
app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# -------------------------------------------------------------------
# 1. Mapper (工人): 下载文件 -> 清洗文本 -> 统计单词
# -------------------------------------------------------------------
@app.activity_trigger(input_name="fileUrl")
def mapper(fileUrl: str) -> dict:
    # 从 URL 下载文本内容
    try:
        response = urllib.request.urlopen(fileUrl)
        text = response.read().decode('utf-8')
    except Exception as e:
        return {"error": str(e)}

    # 清洗文本: 转小写，只保留字母
    words = re.findall(r'[a-z]+', text.lower())
    
    # 统计单词 (返回一个字典，例如 {'the': 100, 'and': 50})
    return dict(Counter(words))

# -------------------------------------------------------------------
# 2. Shuffler (汇总): 接收所有 Mapper 的结果 -> 合并成一个大字典
# -------------------------------------------------------------------
@app.activity_trigger(input_name="results")
def shuffler(results: list) -> dict:
    total_counts = Counter()
    for partial_result in results:
        total_counts.update(partial_result)
    return dict(total_counts)

# -------------------------------------------------------------------
# 3. Master (指挥官): 编排整个流程
# -------------------------------------------------------------------
@app.orchestration_trigger(context_name="context")
def master_orchestrator(context: df.DurableOrchestrationContext):
    
    # ⚠️⚠️⚠️【请修改这里】⚠️⚠️⚠️
    # 把下面的 <你的存储账户名> 换成你刚才在 Azure 上看到的那个名字 (比如 mapreducelab2xxx)
    storage_account_name = "rglab2function9d37"
    container_name = "input"
    
    # 这里列出你刚才上传的文件名 (请确保文件名完全一致！)
    file_list = [
        "mrinput-1.txt", 
        "mrinput-2.txt",
        "mrinput-3.txt",
        "mrinput-4.txt"
    ]

    # 构建完整的 URL 列表
    file_urls = [f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{f}" for f in file_list]

    # --- MAP 阶段: 并发启动所有 Mapper ---
    tasks = []
    for url in file_urls:
        tasks.append(context.call_activity("mapper", url))
    
    # 等待所有 Mapper 完成
    mapped_results = yield context.task_all(tasks)

    # --- REDUCE (Shuffle) 阶段: 汇总结果 ---
    final_result = yield context.call_activity("shuffler", mapped_results)

    return final_result

# -------------------------------------------------------------------
# 4. HTTP Starter: 外部触发器 (用来启动 Master)
# -------------------------------------------------------------------
@app.route(route="orchestrators/master_orchestrator")
@app.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client: df.DurableOrchestrationClient):
    # ⚠️ 关键点 1: 加上 await
    instance_id = await client.start_new("master_orchestrator", None, None)
    logging.info(f"Started orchestration with ID = '{instance_id}'.")
    return client.create_check_status_response(req, instance_id)