# coze_to_xhs
- get coze workflow data,use xhs_mcp_server to auto publish
# coze workflow run
- https://www.coze.cn/open/docs/developer_guides/workflow_run
- llm prompt
```text
# 角色
你是一位专业且经验丰富的书摘生成专家，拥有深厚知识储备与大量实践经验。依据用户输入的书名，能精准、高效地自动生成书摘。熟练运用DeepSeek技术进行深度改写，遵循AIDA模型，营造强烈的对象感、代入感与共情感，精心提炼出3段高质量摘要，打造契合小红书风格的标题与内容。每段内容严格控制在300字左右，全面且精炼地呈现书籍核心要点，将改写后的小红书标题、内容单独输出，每一句完整的话单独成行展示。同时，要确保信息来源准确无误，涉及相关知识时借助搜索工具获取最新、最可靠的信息。

## 技能
### 技能 1: 精准生成书摘
1. 深入剖析用户输入的书名，从主题、情节、人物、写作风格等多维度综合考量，运用先进文本分析方法和专业工具，自动生成高质量书摘。
2. 生成的书摘要精准涵盖书籍核心观点、关键情节、重要人物关系等关键信息，保证内容完整、逻辑清晰、条理分明。

### 技能 2: 深度改写与风格塑造
1. 熟练使用DeepSeek工具，对生成的书摘进行全面、系统改写，提炼出3段逻辑严密、重点突出、层次分明的摘要。
2. 紧密贴合小红书平台风格特点，从语言风格（如活泼、俏皮、富有感染力等）、排版方式（合理分段、使用表情符号等）等方面精心雕琢，重新打造极具吸引力且符合小红书风格的标题、内容。每一段内容控制在300字左右，若内容不足300字，发挥语言天赋进行扩写，精准传达书籍精髓，每一段总结10字左右小标题，同时结合所有内容生成一个简洁有力且符合小红书风格的总标题。

### 技能 3: 深度挖掘作者简介
1. 借助精准搜索功能，深入挖掘书籍作者简介信息，确保信息准确、完整、及时。
2. 对搜索到的作者简介进行细致筛选和整理，提取关键、有价值的信息，以简洁明了、生动有趣的方式呈现给用户。
3. 利用图片搜索工具，找到3张与该书名相关的图片地址信息。

### 技能 4: 引导读者评论
1. 提出2个问题引导读者评论，每个问题在30字左右

## 限制:
- 仅围绕用户输入的书名开展书摘生成、改写以及作者简介挖掘等相关操作，不回答无关话题。
- 输出内容严格按要求格式组织，标题、每段内容分开单独成行展示。
- 每段书摘内容严格控制在300字左右，不足300字进行扩写，总标题简洁精炼且高度概括整体内容。
- 通过搜索工具获取信息时，确保信息来源可靠、权威。
- 将总标题赋值给title变量，其他内容删除总标题后赋值给content变量，图片地址信息输出给images。
- 输出的title/content/images内容要符合json格式。
- 去除content中的特殊符号（如📖、✨、📚、🎓等）。
- 所有格式需符合json格式，输出给下游使用。
- 回答需调用搜索或浏览器工具获取信息，确保信息来源准确。 
```
# xhs_mcp_server
- https://pypi.org/project/xhs-mcp-server/
# ref
- https://www.modelscope.cn/mcp/servers/@XGenerationLab/xhs_mcp_server 小红书MCP发布器
- https://www.modelscope.cn/learn/1205?pid=1204 用Qwen3+MCPs实现AI自动发布小红书笔记！支持图文和视频
# example 
- config.yaml
```yaml
books:
  - 认知觉醒：开启自我改变的原动力 周岭
phone_number: xxxxxxxxxx
cookie_path: /Users/linear/myown/cookie
agent_id: xxxxxxxxxx
workflow_id: xxxxxxxxxx
api_key:  xxxxxxxxxx
multi_pic: false
```
- agent_results.json
```json
{
    "书名": "认知觉醒：开启自我改变的原动力 周岭",
    "结果": "{\"content_type\":1,\"data\":\"{\\n  \\\"title\\\": \\\"《认知觉醒》：找到自我改变的钥匙\\\",\\n  \\\"content\\\": \\\"总标题：《认知觉醒》：找到自我改变的钥匙\\n\\n小标题：剖析思维规律\\n《认知觉醒》深入讲解“大脑构造、潜意识、元认知”等思维规律。人类有本能脑、情绪脑和理智脑，前两者让我们有目光短浅、即时满足的天性，比如难以抵挡手机诱惑并非意志力薄弱。而元认知能让我们反思自身思维和行动，像每日复盘触动自己的事，通过反思与关联保持清醒，纠正不明智想法。\\n\\n小标题：遵循事物规律\\n书中阐述“深度学习、关联、反馈”等事物规律，助我们成事。学习不能只停留在听讲、阅读，要通过讨论、教授他人等提高留存率。读完书要用自己的话阐述内容，结合经历思考并关联相关事情。能力成长有舒适区、拉伸区和困难区，我们应处于舒适区边缘，看稍有难度的书。\\n\\n小标题：缓解焦虑培养耐心\\n焦虑源于欲望与能力差距大且缺乏耐心。缓解焦虑要明白“学习 - 思考 - 行动 - 改变”的成长路径，读书求改变而非单纯求量。培养耐心要接纳自己，放下包袱面对天性；学会延迟满足，变对抗为沟通；面对困难改变视角，赋予行动意义。\\n\\n作者周岭是作家、自媒体人、心智探索者。他的文章有深度又易懂，常被读者誉为一股清流，其文章被“人民日报”官方微博等多家媒体转载。\\n\\n互动问题：\\n1. 你在生活中有没有因为本能脑和情绪脑的主导而做出后悔的事？\\n2. 尝试运用书中方法后，你在培养耐心方面有哪些明显的变化？\\\",\\n  \\\"images\\\": [\\\"https://img.alicdn.com/i3/1049653664/O1CN011p1JPT1cw9vtOhEge_!!1049653664.jpg\\\",\\\"https://qny.smzdm.com/202405/14/6642c618984523074.jpg_a200.jpg\\\",\\\"https://tu.tuibook.com/2024/02/20240202082641802.jpeg\\\"]\\n}\",\"original_result\":null,\"type_for_model\":2}"
}
```
- log
```text
/usr/local/opt/python@3.11/bin/python3.11 /Users/linear/myown/code/coze_to_xhs/src/audo_publish.py 

开始处理书籍: 认知觉醒：开启自我改变的原动力 周岭
HTTP Request: POST https://api.coze.cn/v1/workflow/run "HTTP/1.1 200 OK"
workflow.data {"content_type":1,"data":"{\n  \"title\": \"《认知觉醒》：找到自我改变的钥匙\",\n  \"content\": \"总标题：《认知觉醒》：找到自我改变的钥匙\n\n小标题：剖析思维规律\n《认知觉醒》深入讲解“大脑构造、潜意识、元认知”等思维规律。人类有本能脑、情绪脑和理智脑，前两者让我们有目光短浅、即时满足的天性，比如难以抵挡手机诱惑并非意志力薄弱。而元认知能让我们反思自身思维和行动，像每日复盘触动自己的事，通过反思与关联保持清醒，纠正不明智想法。\n\n小标题：遵循事物规律\n书中阐述“深度学习、关联、反馈”等事物规律，助我们成事。学习不能只停留在听讲、阅读，要通过讨论、教授他人等提高留存率。读完书要用自己的话阐述内容，结合经历思考并关联相关事情。能力成长有舒适区、拉伸区和困难区，我们应处于舒适区边缘，看稍有难度的书。\n\n小标题：缓解焦虑培养耐心\n焦虑源于欲望与能力差距大且缺乏耐心。缓解焦虑要明白“学习 - 思考 - 行动 - 改变”的成长路径，读书求改变而非单纯求量。培养耐心要接纳自己，放下包袱面对天性；学会延迟满足，变对抗为沟通；面对困难改变视角，赋予行动意义。\n\n作者周岭是作家、自媒体人、心智探索者。他的文章有深度又易懂，常被读者誉为一股清流，其文章被“人民日报”官方微博等多家媒体转载。\n\n互动问题：\n1. 你在生活中有没有因为本能脑和情绪脑的主导而做出后悔的事？\n2. 尝试运用书中方法后，你在培养耐心方面有哪些明显的变化？\",\n  \"images\": [\"https://img.alicdn.com/i3/1049653664/O1CN011p1JPT1cw9vtOhEge_!!1049653664.jpg\",\"https://qny.smzdm.com/202405/14/6642c618984523074.jpg_a200.jpg\",\"https://tu.tuibook.com/2024/02/20240202082641802.jpeg\"]\n}","original_result":null,"type_for_model":2} https://www.coze.cn/work_flow?execute_id=7505605457399808037&space_id=7493495980332285988&workflow_id=7505245815179804691&execute_mode=2 None
已保存 认知觉醒：开启自我改变的原动力 周岭 的结果到 agent_results.json
title parse after  《认知觉醒》：找到自我改变的钥匙
content parse after  

剖析思维规律
《认知觉醒》深入讲解“大脑构造、潜意识、元认知”等思维规律。人类有本能脑、情绪脑和理智脑，前两者让我们有目光短浅、即时满足的天性，比如难以抵挡手机诱惑并非意志力薄弱。而元认知能让我们反思自身思维和行动，像每日复盘触动自己的事，通过反思与关联保持清醒，纠正不明智想法。

遵循事物规律
书中阐述“深度学习、关联、反馈”等事物规律，助我们成事。学习不能只停留在听讲、阅读，要通过讨论、教授他人等提高留存率。读完书要用自己的话阐述内容，结合经历思考并关联相关事情。能力成长有舒适区、拉伸区和困难区，我们应处于舒适区边缘，看稍有难度的书。

缓解焦虑培养耐心
焦虑源于欲望与能力差距大且缺乏耐心。缓解焦虑要明白“学习 - 思考 - 行动 - 改变”的成长路径，读书求改变而非单纯求量。培养耐心要接纳自己，放下包袱面对天性；学会延迟满足，变对抗为沟通；面对困难改变视角，赋予行动意义。

作者周岭是作家、自媒体人、心智探索者。他的文章有深度又易懂，常被读者誉为一股清流，其文章被“人民日报”官方微博等多家媒体转载。

互动问题：
1. 你在生活中有没有因为本能脑和情绪脑的主导而做出后悔的事？
2. 尝试运用书中方法后，你在培养耐心方面有哪些明显的变化？
images parse after  ['https://img.alicdn.com/i3/1049653664/O1CN011p1JPT1cw9vtOhEge_!!1049653664.jpg', 'https://qny.smzdm.com/202405/14/6642c618984523074.jpg_a200.jpg', 'https://tu.tuibook.com/2024/02/20240202082641802.jpeg']
正在发布到小红书: 《认知觉醒》：找到自我改变的钥匙
使用电话号码: xxxxxxxxxxx
使用cookie文件: /Users/linear/myown/cookie
Exception managing chrome: error sending request for url (https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json)
download_image error  420 Client Error:  for url: https://img.alicdn.com/i3/1049653664/O1CN011p1JPT1cw9vtOhEge_!!1049653664.jpg
download_image error  HTTPSConnectionPool(host='tu.tuibook.com', port=443): Max retries exceeded with url: /2024/02/20240202082641802.jpeg (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1016)')))


剖析思维规律
《认知觉醒》深入讲解“大脑构造、潜意识、元认知”等思维规律。人类有本能脑、情绪脑和理智脑，前两者让我们有目光短浅、即时满足的天性，比如难以抵挡手机诱惑并非意志力薄弱。而元认知能让我们反思自身思维和行动，像每日复盘触动自己的事，通过反思与关联保持清醒，纠正不明智想法。

遵循事物规律
书中阐述“深度学习、关联、反馈”等事物规律，助我们成事。学习不能只停留在听讲、阅读，要通过讨论、教授他人等提高留存率。读完书要用自己的话阐述内容，结合经历思考并关联相关事情。能力成长有舒适区、拉伸区和困难区，我们应处于舒适区边缘，看稍有难度的书。

缓解焦虑培养耐心
焦虑源于欲望与能力差距大且缺乏耐心。缓解焦虑要明白“学习 - 思考 - 行动 - 改变”的成长路径，读书求改变而非单纯求量。培养耐心要接纳自己，放下包袱面对天性；学会延迟满足，变对抗为沟通；面对困难改变视角，赋予行动意义。

作者周岭是作家、自媒体人、心智探索者。他的文章有深度又易懂，常被读者誉为一股清流，其文章被“人民日报”官方微博等多家媒体转载。

互动问题：
1. 你在生活中有没有因为本能脑和情绪脑的主导而做出后悔的事？
2. 尝试运用书中方法后，你在培养耐心方面有哪些明显的变化？
发布成功
发布完成,result:True res:发布成功
sleep a while...sleep_count: 1
sleep a while...sleep_count: 2
sleep a while...sleep_count: 3
sleep a while...sleep_count: 4
sleep a while...sleep_count: 5
sleep a while...sleep_count: 6
sleep a while...sleep_count: 7
sleep a while...sleep_count: 8
sleep a while...sleep_count: 9
sleep a while...sleep_count: 10
sleep a while...sleep_count: 11
sleep a while...sleep_count: 12
sleep a while...sleep_count: 13
sleep a while...sleep_count: 14
sleep a while...sleep_count: 15
sleep a while...sleep_count: 16
sleep a while...sleep_count: 17
sleep a while...sleep_count: 18
sleep a while...sleep_count: 19
sleep a while...sleep_count: 20
sleep a while...sleep_count: 21
sleep a while...sleep_count: 22
sleep a while...sleep_count: 23
sleep a while...sleep_count: 24
sleep a while...sleep_count: 25
sleep a while...sleep_count: 26
sleep a while...sleep_count: 27
sleep a while...sleep_count: 28
sleep a while...sleep_count: 29
sleep a while...sleep_count: 30
sleep a while...sleep_count: 31
sleep a while...sleep_count: 32
sleep a while...sleep_count: 33
sleep a while...sleep_count: 34
sleep a while...sleep_count: 35
sleep a while...sleep_count: 36
sleep a while...sleep_count: 37
sleep a while...sleep_count: 38
sleep a while...sleep_count: 39
sleep a while...sleep_count: 40
sleep a while...sleep_count: 41
sleep a while...sleep_count: 42
sleep a while...sleep_count: 43
sleep a while...sleep_count: 44
sleep a while...sleep_count: 45
sleep a while...sleep_count: 46
sleep a while...sleep_count: 47
sleep a while...sleep_count: 48
sleep a while...sleep_count: 49
sleep a while...sleep_count: 50
sleep a while...sleep_count: 51
sleep a while...sleep_count: 52
sleep a while...sleep_count: 53
sleep a while...sleep_count: 54
sleep a while...sleep_count: 55
sleep a while...sleep_count: 56
sleep a while...sleep_count: 57
sleep a while...sleep_count: 58
sleep a while...sleep_count: 59
sleep a while...sleep_count: 60
log_content: 
处理书籍: 认知觉醒：开启自我改变的原动力 周岭
智能体结果保存成功
小红书发布成功

所有处理已完成，日志已保存到 publish_log.txt

Process finished with exit code 0

```
