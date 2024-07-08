import openai


def deepseek(messages):

    client = openai.OpenAI(
        base_url="https://api.deepseek.com",
        api_key="***", #填写自己对应的api_key,需在官网上购买，deepseek比较便宜且够用
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        max_tokens=64
    ).choices[0].message.content

    messages.append({'role': 'assistant', 'content': response})

    return response

