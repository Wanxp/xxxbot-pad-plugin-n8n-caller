# xxxbot-pad-plugin-n8n-caller
xxxbot-pad插件，用于wechat/微信消息回调n8n的webhook接口

## 功能
使用该插件可以将消息推送至n8n的Webhook中。
## 使用方法
### n8n配置
1. 在n8n中创建一个Webhook节点，设置Webhook的path。
2. 设置请求方法为POST
3. 设置一个鉴权方式 目前仅支持Basic Auth、Header Auth、None
4. 设置一个请求体格式 目前仅支持JSON、Form Data
### 插件配置
```toml
#匹配消息的发送者wxid,只要这些才会触发回调,可修改为你需要的前缀
sender=["wxid1","wxid2","wxid3"]
#匹配消息的前缀,只要这个前缀的才会触发回调,可修改为你需要的前缀
message-keyword=["n:","N:","n8n:","N8N:","n：","N：","n8n：","N8N："]
# n8n的webhook地址, 注意只支持post请求，消息体会作为请求体发送
n8n-webhook-url = "https://n8n.example.com/webhook/这里是你设置的path"
# 支持 Basic Auth, Header Auth, None
auth-type = "Header Auth"
# Basic Auth 时当前值为用户名(username)
# Header Auth时为HeaderName,
# None 无需填写
auth-key= "Authorization"
# Basic Auth 时当前值为密码(password)
# Header Auth时为HeaderValue,
# None 无需填写
auth-value= "sk-0ZxCTjjCsPoZEK"
```


### n8n接收到的消息格式案例如下
```json
[
  {
    "headers": {
      "connection": "keep-alive",
      "host": "n8n.example.com",
      "x-forwarded-scheme": "https",
      "x-forwarded-proto": "https",
      "x-forwarded-for": "**.**.**.**",
      "x-real-ip": "**.**.**.**",
      "content-length": "662",
      "user-agent": "python-requests/2.32.3",
      "accept-encoding": "gzip, deflate, br",
      "accept": "*/*",
      "content-type": "application/json",
      "authorization": "sk-0ZxCAjHul8tTjjCsPoZEK"
    },
    "params": {},
    "query": {},
    "body": {
      "MsgId": 176701310,
      "ToUserName": {
        "string": "wxid_id"
      },
      "MsgType": 1,
      "Content": "这里是排除前缀后的消息",
      "Status": 3,
      "ImgStatus": 1,
      "ImgBuf": {
        "iLen": 0
      },
      "CreateTime": 1747217407,
      "MsgSource": "<msgsource>\n\t<pua>1</pua>\n\t<alnode>\n\t\t<cf>2</cf>\n\t</alnode>\n\t<eggIncluded>1</eggIncladfdfdf</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n",
      "PushContent": "张三 : n：a：你好",
      "NewMsgId": 4369693081088619500,
      "MsgSeq": 709744630,
      "FromWxid": "wxid_id",
      "ToWxid": "",
      "SenderWxid": "wxid_id",
      "IsGroup": false,
      "Ats": []
    },
    "webhookUrl": "https://n8n.example.com/webhook/webhook/wechat",
    "executionMode": "test"
  }
]

```


### n8n 处理demo
1. 打开n8n
2. 将下面的json复制保存到本地文件，并以json作为后缀名
3. 在n8n中导入该json文件
4. 开启并配置当前插件
5. 发送消息"n:a:你好"

```json
{
  "name": "wechat-ace-call",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "wechat",
        "authentication": "headerAuth",
        "responseMode": "responseNode",
        "options": {}
      },
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [
        -300,
        -20
      ],
      "id": "765c2eda-0403-4fc4-a09d-f3a73b5e1148",
      "name": "Webhook",
      "webhookId": "280a296b-62d0-49ff-b006-df0efd88785c",
      "credentials": {
        "httpHeaderAuth": {
          "id": "7qBG3HNelMInMFxg",
          "name": "wechat-auth-authorization"
        }
      }
    },
    {
      "parameters": {
        "jsCode": "// Loop over input items and add a new field called 'myNewField' to the JSON of each one\nconst data =  $('Webhook').first().json.body\nconst typeMap = $input.first().json.msgTypeMap\nfunction getType(msg) {\n  if (!msg) {\n    return {\"msg\": msg, \"type\": \"unknown\"}\n  }\n  const msgTy = msg.substring(0, Math.min(20, msg.length))\n  let result = []\n  let spiltStr = ''\n  if (msgTy.includes(':')) {\n    result = msg.split(\":\");\n    spiltStr = ':'\n  } else if (msgTy.includes('：')) {\n    result = msg.split(\"：\");\n    spiltStr = '：'\n  } else {\n    result = []\n  }\n  let typeKeyWord = ''\n  if (result.length >= 2) {\n    typeKeyWord = result[0]\n  }\n  if (typeKeyWord == '') {\n    return {\"msg\": msg, \"type\": \"unknown\"}\n  }\n  typeKeyWord = typeKeyWord.toLocaleLowerCase()\n  for (const row of typeMap) {\n    if (row['keyWord'].some(k => k === typeKeyWord)) {\n      const matchData = row['keyWord'].find(k => k === typeKeyWord)\n      return {\"msg\": msg.substring(msg.indexOf(typeKeyWord + spiltStr), msg.length) , \"type\": row['name']}\n    }\n  }\n  return {\"msg\": msg, \"type\": \"unknown\"}\n}\n\n\n\nconst msgType = getType(data.Content)\nreturn {\n  \"sender\": data.sender,\n  \"msg\": msgType['msg'],\n  \"timestamp\": $now.toMillis(),\n  \"type\": msgType['type'],\n}"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        140,
        -20
      ],
      "id": "32509d74-5d94-494a-af4e-40a1644989dc",
      "name": "提取消息",
      "executeOnce": true
    },
    {
      "parameters": {
        "rules": {
          "values": [
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "leftValue": "",
                  "typeValidation": "strict",
                  "version": 2
                },
                "conditions": [
                  {
                    "leftValue": "={{ $json.type }}",
                    "rightValue": "obsidian",
                    "operator": {
                      "type": "string",
                      "operation": "equals"
                    },
                    "id": "1fe7a907-6d5b-4da4-ab1e-9ee8f13c30c3"
                  }
                ],
                "combinator": "and"
              },
              "renameOutput": true,
              "outputKey": "obsidian"
            },
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "leftValue": "",
                  "typeValidation": "strict",
                  "version": 2
                },
                "conditions": [
                  {
                    "id": "d6bc07fd-44a6-49f7-93f7-a27c72cd76bf",
                    "leftValue": "={{ $json.type }}",
                    "rightValue": "ai",
                    "operator": {
                      "type": "string",
                      "operation": "equals"
                    }
                  }
                ],
                "combinator": "and"
              },
              "renameOutput": true,
              "outputKey": "ai"
            },
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "leftValue": "",
                  "typeValidation": "strict",
                  "version": 2
                },
                "conditions": [
                  {
                    "id": "9b0e79a2-53a6-4825-be9c-dc48ea208028",
                    "leftValue": "={{ $json.type }}",
                    "rightValue": "unknown",
                    "operator": {
                      "type": "string",
                      "operation": "equals"
                    }
                  }
                ],
                "combinator": "and"
              },
              "renameOutput": true,
              "outputKey": "unknown"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.switch",
      "typeVersion": 3.2,
      "position": [
        420,
        -40
      ],
      "id": "2e751358-3c73-4ded-bbba-28b34bb5204d",
      "name": "选择处理"
    },
    {
      "parameters": {
        "operation": "toText",
        "sourceProperty": "content",
        "options": {
          "fileName": "={{ $json.fileName }}"
        }
      },
      "type": "n8n-nodes-base.convertToFile",
      "typeVersion": 1.1,
      "position": [
        900,
        -120
      ],
      "id": "9fc21314-6a71-45b7-9375-49284c4744c1",
      "name": "转换成文件"
    },
    {
      "parameters": {
        "operation": "write",
        "fileName": "={{ $('生成Obsidian笔记').item.json.path }}",
        "dataPropertyName": "=data",
        "options": {
          "append": false
        }
      },
      "type": "n8n-nodes-base.readWriteFile",
      "typeVersion": 1,
      "position": [
        1080,
        -120
      ],
      "id": "99e16198-181a-43cc-aabf-b4ac47a50eed",
      "name": "保存文件"
    },
    {
      "parameters": {
        "jsCode": "\n// 自定义格式化日期的函数\nfunction formatDate(date, format) {\n    const pad = (num) => String(num).padStart(2, '0');\n    return format\n        .replace(/yyyy/g, date.getFullYear())\n        .replace(/MM/g, pad(date.getMonth() + 1))\n        .replace(/dd/g, pad(date.getDate()))\n        .replace(/HH/g, pad(date.getHours()))\n        .replace(/mm/g, pad(date.getMinutes()))\n        .replace(/ss/g, pad(date.getSeconds()));\n}\n\n\n// 假设 $input.first().json.msg 是从某个数据源获取的\nconst inputMsg = $input.first().json.msg.replaceAll('ob:', '').replaceAll('ob：', '').replaceAll('OB:', '').replaceAll('OB：', '').replaceAll('Ob：', '').replaceAll('Ob：', ''); // 替换为实际获取的消息\nconst now = new Date();\nconst id = formatDate(now, 'yyyyMMddHHmmss');\nconst start = 0; // 根据您的需要设置\nconst minLength = 10; // 根据您的需要设置\nconst title = `${id}_${inputMsg.slice(start, Math.min(minLength, inputMsg.length))}`;\nconst fileName = `${title}.md`\nconst filePath = `/home/wanxp/Syncthing/obsidian/thought_box/${title}.md`;\n\nconst markdownData = `---\ntags: \n - thought_box\n - 想法\n - 素材\n - ${formatDate(now, 'yyyy_MM_dd')}\ncreateTime: ${formatDate(now, 'yyyy-MM-ddTHH:mm:ss')}\ncreateBy: wanxuping\nid: ${id}\nsource: 微信\n---\n\n---\n### 想法\n\n${inputMsg}\n`;\n\nconsole.log(`path: ${filePath}\\ndata: ${markdownData}`);\n\nreturn {\n  \"fileName\": fileName,\n  \"path\": filePath,\n  \"content\": markdownData\n}\n"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        720,
        -120
      ],
      "id": "3f90ab30-6aac-47c9-bf3e-2ad689ed03f4",
      "name": "生成Obsidian笔记",
      "executeOnce": true
    },
    {
      "parameters": {},
      "type": "@n8n/n8n-nodes-langchain.chainLlm",
      "typeVersion": 1.6,
      "position": [
        920,
        160
      ],
      "id": "9a4ccf80-3e9e-46b5-b54d-6272c8979e20",
      "name": "Basic LLM Chain"
    },
    {
      "parameters": {
        "jsCode": "\nconst inputMsg = $input.first().json.msg.replaceAll('a:', '').replaceAll('A：', '').replaceAll('a:', '').replaceAll('A：', '').replaceAll('ai：', '').replaceAll('ai：', '').replaceAll('AI:', '').replaceAll('Ai：', '').replaceAll('aI：', '').replaceAll('ai：', ''); // 替换为实际获取的消息\n\n\nreturn {\n  \"chatInput\": inputMsg\n}\n"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        720,
        80
      ],
      "id": "6bafc314-ea2c-4bf0-8635-0cf80c3c87a7",
      "name": "截取非关键词部分",
      "executeOnce": true
    },
    {
      "parameters": {
        "respondWith": "text",
        "responseBody": "={{ $json.text }}",
        "options": {}
      },
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [
        1260,
        160
      ],
      "id": "2bcfa28f-aa87-46f3-afa5-2b0de35a4cbf",
      "name": "响应"
    },
    {
      "parameters": {
        "respondWith": "text",
        "responseBody": "记录成功",
        "options": {}
      },
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [
        680,
        -380
      ],
      "id": "2fdd2417-32ef-4558-a00d-4cc1f08093c5",
      "name": "响应1"
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "0ee378cf-5804-405c-9471-2f992154315c",
              "name": "msgTypeMap",
              "value": "={{[{\"name\": \"obsidian\", \"keyWord\": [\"ob\"]}, {\"name\": \"ai\", \"keyWord\": [\"ai\",\"a\"]},]}}",
              "type": "array"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [
        -80,
        -20
      ],
      "id": "04c49233-0a40-427e-9721-42d691161894",
      "name": "变量声明"
    },
    {
      "parameters": {
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmChatDeepSeek",
      "typeVersion": 1,
      "position": [
        920,
        320
      ],
      "id": "f6ebb77e-79a0-48b7-b0bb-33b085423572",
      "name": "DeepSeek Chat Model",
      "credentials": {
        "deepSeekApi": {
          "id": "pewGn9ABuleNUiC8",
          "name": "DeepSeek account"
        }
      }
    }
  ],
  "pinData": {},
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "变量声明",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "提取消息": {
      "main": [
        [
          {
            "node": "选择处理",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "选择处理": {
      "main": [
        [
          {
            "node": "生成Obsidian笔记",
            "type": "main",
            "index": 0
          },
          {
            "node": "响应1",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "截取非关键词部分",
            "type": "main",
            "index": 0
          }
        ],
        []
      ]
    },
    "转换成文件": {
      "main": [
        [
          {
            "node": "保存文件",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "生成Obsidian笔记": {
      "main": [
        [
          {
            "node": "转换成文件",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Basic LLM Chain": {
      "main": [
        [
          {
            "node": "响应",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "截取非关键词部分": {
      "main": [
        [
          {
            "node": "Basic LLM Chain",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "响应1": {
      "main": [
        []
      ]
    },
    "变量声明": {
      "main": [
        [
          {
            "node": "提取消息",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "DeepSeek Chat Model": {
      "ai_languageModel": [
        [
          {
            "node": "Basic LLM Chain",
            "type": "ai_languageModel",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "f51cf259-bc8b-4275-9dbc-d2e3a475d858",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "ae2f776acc4b3d7ec013ba736ede90afd36cb5875ac14f4f133a6f823f5a8ae6"
  },
  "id": "mhqYZZpI3Nq2PyOD",
  "tags": []
}
```