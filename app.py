from flask import Flask,render_template,url_for,request
import json
from http import HTTPStatus
import dashscope
import re
dashscope.api_key="sk-d81529d7b5f247858c6c5899d4ad24ab"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result',methods=['GET','POST'])
def result():
    if request.method == 'POST':
        res=request.form['text']
        def convert_to_tree_data(text):
            prompt = '''
            文本转换为嵌套JSON格式，示例格式如下：
{
    "name": "根节点名称",
    "children": [
        {
            "name": "子节点1",
            "children": [
                {
                    "name": "子节点1-1",
                    "children": [
                        {
                            "name": "子节点1-1-1"
                        },
                        {
                            "name": "子节点1-1-2"
                        }
                    ]
                },
                {
                    "name": "子节点1-2",
                    "children": [
                        {
                            "name": "子节点1-2-1"
                        }
                    ]
                }
            ]
        },
        {
            "name": "子节点2",
            "children": [
                {
                    "name": "子节点2-1",
                    "children": [
                        {
                            "name": "子节点2-1-1"
                        },
                        {
                            "name": "子节点2-1-2",
                            "children": [
                                {
                                    "name": "子节点2-1-2-1"
                                },
                                {
                                    "name": "子节点2-1-2-2"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "子节点2-2"
                }
            ]
        }
    ]
}
,具体内容示例如下
{
    "name": "微流控芯片",
    "children": [
        {
            "name": "工作原理",
            "children": [
                {
                    "name": "两相流体保持平行流动，通过优化通道几何结构和控制流体组成与流速维持层流或生成微液滴"
                }
            ]
        },
        {
            "name": "驱动方式分类",
            "children": [
                {
                    "name": "机械力驱动",
                    "children": [
                        { "name": "压力推动式" },
                        { "name": "压电驱动" }
                    ]
                },
                {
                    "name": "非机械力驱动",
                    "children": [
                        { "name": "数字化微流控" },
                        { "name": "液滴微流控" },
                        { "name": "重力推动式" }
                    ]
                }
            ]
        },
        {
            "name": "材料分类",
            "children": [
                {
                    "name": "常见材料",
                    "children": [
                        { "name": "单晶硅片" },
                        { "name": "分子聚合物" }
                    ]
                },
                {
                    "name": "现代材料",
                    "children": [
                        { "name": "聚二甲基硅氧烷（PDMS）" },
                        { "name": "水凝胶" }
                    ]
                },
                {
                    "name": "其他材料",
                    "children": [
                        { "name": "聚碳酸酯（PC）" },
                        { "name": "3D打印技术" }
                    ]
                },
                {
                    "name": "三级分支主题特性",
                    "children": [
                        { "name": "透气性" },
                        { "name": "成本低" }
                    ]
                }
            ]
        },
        {
            "name": "制备方法",
            "children": [
                { "name": "热压法" },
                { "name": "软刻蚀法" }
            ]
        }
    ]
}


            我现在想根据以下文本生成一个思维导图，请参考以上示例，梳理文本逻辑，，将以下文本转换为上面示例中的JSON格式：
            ''' + text

            def call_with_prompt():
                response = dashscope.Generation.call(
                    model=dashscope.Generation.Models.qwen_max,
                    prompt=prompt
                )
                # 如果调用成功，则打印模型的输出
                if response.status_code == HTTPStatus.OK:
                    print(response)
                    json_res = response.output.text
                    print(json_res)
                    pattern = r'```json\n(.*?)\n```'
                    matched_text = re.search(pattern, json_res, re.DOTALL)
                    if matched_text:
                        # group(1)包含的是第一个括号内匹配的内容
                        extracted_json = matched_text.group(1)
                        print(extracted_json)
                        return extracted_json
                    else:
                        print("No match found.")
                        return "No match found."
                # 如果调用失败，则打印出错误码与失败信息
                else:
                    print(response.code)
                    print(response.message)

            #if __name__ == '__main__':
            json_res = call_with_prompt()
                #json_res = json.loads(json_res)

            return json_res

        tree_data = json.loads(convert_to_tree_data(res))
        print(tree_data)
        return render_template('result.html',res=tree_data)


if __name__ ==   '__main__':
    app.run(debug=True)
