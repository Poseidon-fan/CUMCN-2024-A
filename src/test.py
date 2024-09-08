import pandas as pd

# 假设你的二维列表如下
data = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# 将二维列表转换为DataFrame
df = pd.DataFrame(data)

# 对DataFrame进行转置操作，使行变为列
df_transposed = df.transpose()

# 将转置后的DataFrame导出为xlsx文件
df_transposed.to_excel("output.xlsx", index=False, header=False)
