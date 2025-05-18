import json
import logging
import os
import re
import time
from typing import Dict, List, Optional

import httpx
import yaml
from cozepy import COZE_CN_BASE_URL
from cozepy import Coze, TokenAuth
from xhs_mcp_server.server import download_image
from xhs_mcp_server.write_xiaohongshu import XiaohongshuPoster

logging.basicConfig(level=logging.DEBUG)


class XiaohongshuAutomation:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.books = self.config.get("books", [])
        self.result_file = self.config.get("result_file", "agent_results.json")
        self.phone_number = self.config.get("phone_number")
        self.cookie_path = self.config.get("cookie_path")
        self.agent_id = self.config.get("agent_id")
        self.workflow_id = self.config.get("workflow_id")
        self.coze_api_token = self.config.get("api_key")
        self.coze_api_base = COZE_CN_BASE_URL
        self.multi_pic = self.config.get("multi_pic")

        if not os.path.exists(self.result_file):
            with open(self.result_file, "w", encoding="utf - 8") as f:
                json.dump([], f)

    def _load_config(self, config_path: str) -> Dict:
        try:
            with open(config_path, "r", encoding="utf - 8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            raise

    def call_agent(self, book_name: str) -> Optional[Dict]:
        try:
            # return "{\"content_type\":1,\"data\":\"{\\n  \\\"title\\\": \\\"《小镇喧嚣》：揭开乡镇政治运作的神秘面纱\\\",\\n  \\\"content\\\": \\\"### 总标题：《小镇喧嚣》：揭开乡镇政治运作的神秘面纱\\n\\n### 摘要一\\n想知道乡镇政治是怎么运作的吗？《小镇喧嚣》带你深入了解。书中以生动笔触描绘了乡镇工作的复杂场景。乡镇干部在政策执行与群众需求间努力平衡。比如在土地征收问题上，既要完成上级任务，又要安抚群众情绪，避免矛盾激化。作者通过大量真实案例，展现出乡镇工作并非一帆风顺，各种利益博弈、观念冲突不断。让我们看到基层政治生态的多面性，理解乡镇干部工作的艰辛与不易，对乡镇政治有全新认识。\\n\\n### 摘要二\\n《小镇喧嚣》里藏着乡镇政治的百态人生。书中人物形象鲜活，有一心为民却面临诸多难题的干部，也有在利益面前摇摆不定的角色。他们的故事串联起乡镇政治运作的脉络。在项目引进过程中，不同立场的人有着不同诉求，有人希望借此发展经济，有人担心破坏环境。这些矛盾冲突推动着情节发展，让我们仿佛置身其中，感受乡镇政治运作中人性的复杂与世事的难料，也看到政策落地背后的重重阻碍。\\n\\n### 摘要三\\n翻开《小镇喧嚣》，如同打开乡镇政治的观察窗口。作者细腻的描写，将乡镇政治运作的细节一一呈现。从会议讨论到实地走访，从解决纠纷到推动发展，全方位展示了乡镇工作的日常。书中还探讨了制度与现实的落差，一些看似完美的政策，在乡镇实施时却困难重重。通过这本书，我们能洞察乡镇政治的深层逻辑，明白基层治理需要不断探索与创新，为理解中国乡村发展提供独特视角。\\\",\\n  \\\"images\\\": [\\\"https://so1.360tres.com/t013c839f08fb43e437.jpg\\\",\\\"https://img.alicdn.com/i2/859515618/O1CN01S4hxR91rN5ttFsn3L_!!859515618.jpg\\\",\\\"https://img.alicdn.com/bao/uploaded/O1CN01Zgjwu21lXjNWuQpaM_!!6000000004829-0-yinhe.jpg\\\"]\\n}\",\"original_result\":null,\"type_for_model\":2}"
            # Init the Coze client through the access_token.
            coze = Coze(auth=TokenAuth(token=self.coze_api_token), base_url=self.coze_api_base)

            # Call the coze.workflows.runs.create method to create a workflow run. The create method
            # is a non-streaming chat and will return a WorkflowRunResult class.
            workflow = coze.workflows.runs.create(
                workflow_id=str(self.workflow_id),
                parameters={"input": book_name}
            )

            print("workflow.data", workflow.data, workflow.debug_url, workflow.execute_id)
            return workflow.data
        except httpx.HTTPError as e:
            print(f"调用智能体失败: {e}")
            return None

    def save_agent_result(self, book_name: str, result: Dict) -> None:
        try:
            with open(self.result_file, "w", encoding="utf-8") as f:
                data = {"书名": book_name, "结果": result}
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"已保存 {book_name} 的结果到 {self.result_file}")
        except Exception as e:
            print(f"保存结果失败: {e}")

    def publish_to_xiaohongshu(self, title: str, content: str, images: List[str]) -> bool:
        # publish
        print(f"正在发布到小红书: {title}")
        print(f"使用电话号码: {self.phone_number}")
        print(f"使用cookie文件: {self.cookie_path}")
        #
        poster = XiaohongshuPoster(self.cookie_path)
        result = False
        try:
            if len(images) > 0 and images[0].startswith("http"):
                # 下载图片
                local_images = []
                for image in images:
                    try:
                        if self.is_valid_image(image):
                            local_image = download_image(image)
                            local_images.append(local_image)
                        else:
                            # 分割URL，去除查询参数（?之后的部分）
                            image_without_query = image.split('?')[0]
                            if self.is_valid_image(image_without_query):
                                local_image = download_image(image_without_query)
                                local_images.append(local_image)
                            else:
                                print("continue,image is not valid image:", image)
                                continue
                    except Exception as exSingle:
                        print("download_image error ", exSingle)
            else:
                local_images = images
            # 暂时兼容 invalid argument: the element can not hold multiple files
            if (self.multi_pic):
                one_local_images = local_images
            else:
                one_local_images = []
                one_local_images.append(local_images[0])

            # 调用小红书工具
            code, info = poster.login_to_publish(title, content, one_local_images)
            poster.close()
            res = info
            result = code
        except Exception as e:
            res = "error login_to_publish:" + str(e)

        # 模拟发布过程
        time.sleep(2)
        print(f"发布完成,result:{result} res:{res}")
        return result

    def is_valid_image(self, filename: str) -> bool:
        """检查文件后缀是否为允许的图片格式"""
        valid_extensions = {'png', 'jpg', 'jpeg', 'webp'}
        ext = filename.lower().split('.')[-1]  # 获取小写后缀
        return ext in valid_extensions

    def process_books(self) -> None:
        log_file = "publish_log.txt"
        log_content = ""
        for book in self.books:
            print(f"\n开始处理书籍: {book}")
            log_content += f"\n处理书籍: {book}\n"
            agent_result = self.call_agent(book)
            if not agent_result:
                log_content += "调用智能体失败\n"
                continue
            self.save_agent_result(book, agent_result)
            log_content += "智能体结果保存成功\n"
            try:
                if isinstance(agent_result, str):
                    agent_result_json = json.loads(agent_result, strict=False)
                raw_data = agent_result_json.get("data", "{}")
                # 将JSON字符串转为字典
                agent_result_data = json.loads(raw_data, strict=False)
                title = agent_result_data.get("title", "")
                # 剔除 Emoji
                title = re.sub(r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF]', '', title)
                print("title parse after ", title)
                # content
                content = agent_result_data.get("content", "")
                content = str(content).replace("------------", "\\n\\n")
                # 剔除标题
                content = content.replace(title, '')
                # 剔除 Emoji
                content = re.sub(r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', '', content)
                # 定义要替换的文本列表
                patterns = [
                    r'✨|📖|📝|🤔',  # 替换 Emoji
                    r'###|总标题[:：]?|小标题[:：]|[分]*标题[:：]?\d*[:：]?|内容[:：]',  # 替换各类标题标记
                    r'书摘\s?[一二三四1234][:：]?|摘要[一二三四1234][:：]?|段落[一二三四1234][:：]?',  # 替换摘要标记
                ]
                # 组合所有模式为单个正则表达式
                pattern = re.compile('|'.join(patterns))

                # 执行替换
                content = pattern.sub('', content)
                #
                print("content parse after ", content)
                # image
                images = agent_result_data.get("images", [])
                print("images parse after ", images)
                if not title or not content:
                    log_content += "智能体返回结果缺少必要字段\n"
                    continue
                count = 0
                while count < 10:
                    success = self.publish_to_xiaohongshu(title, content, images)
                    if success:
                        log_content += "小红书发布成功\n"
                        break
                    else:
                        count += 1
                        log_content += "小红书发布失败 " + str(count) + "\n"

            except Exception as e:
                log_content += f"处理过程中出错: {e}\n"
            # 防止被限流
            sleep_count = 0
            while sleep_count < 60:
                time.sleep(1)
                sleep_count += 1
                print("sleep a while...sleep_count:", sleep_count)
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(log_content)
        print("log_content:", log_content)
        print(f"所有处理已完成，日志已保存到 {log_file}")


if __name__ == "__main__":
    try:
        automation = XiaohongshuAutomation()
        automation.process_books()
    except Exception as e:
        print(f"系统运行出错: {e}")
