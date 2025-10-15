import pandas as pd
import random
import datetime


def generate_new_action_table(file_path, n, m):
    """
    Generate a new action table based on the input Excel file, filtering obj == 0 actions.

    Args:
        file_path (str): Path to the input Excel file.
        n (int): Number of repetitions for each action.
        m (int): Number of actions per block.

    Returns:
        str: The file name of the generated new action table.
    """
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 筛选 obj == 0 的行
    filtered_data = df[df['obj'] == 0]

    # 将动作重复 n 次
    repeated_actions = filtered_data.loc[filtered_data.index.repeat(n)].reset_index(drop=True)

    # 随机打乱顺序（包括所有列）
    shuffled_actions = repeated_actions.sample(frac=1, random_state=39).reset_index(drop=True)

    # 分割为多个 block，每个 block 包含 m 个动作
    shuffled_actions['blockNumber'] = (shuffled_actions.index // m) + 1

    # 保存新的表格
    current_time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    new_file_name = f"AOE_filtered_table_{current_time_str}.xlsx"
    shuffled_actions.to_excel(new_file_name, index=False)

    print(f"New action table generated and saved as: {new_file_name}")
    return new_file_name


# 参数设置
file_path = 'stim_table_initial.xlsx'  # 输入文件路径
n = 4  # 动作重复次数
m = 8  # 每个 block 的动作数

# 调用函数生成新的动作表格
new_action_table = generate_new_action_table(file_path, n, m)
print(f"Generated table: {new_action_table}")
