import pandas as pd
import datetime

def generate_obj_one_action_table(file_path, n):
    """
    Generate a new action table based on the input Excel file, for obj == 1 actions.

    Args:
        file_path (str): Path to the input Excel file.
        n (int): Number of repetitions for each action.

    Returns:
        str: The file name of the generated new action table.
    """
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 筛选 obj == 1 的行
    filtered_data = df[df['obj'] == 1]

    # 将动作重复 n 次
    repeated_actions = filtered_data.loc[filtered_data.index.repeat(n)].reset_index(drop=True)

    # 增加 blockNumber 列，每个动作是一个独立的 block
    repeated_actions['blockNumber'] = (repeated_actions.index // n) + 1

    # 保存新的表格
    current_time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    new_file_name = f"AOE_obj_one_table_{current_time_str}.xlsx"
    repeated_actions.to_excel(new_file_name, index=False)

    print(f"New action table for obj=1 generated and saved as: {new_file_name}")
    return new_file_name


# 参数设置
file_path = 'stim_table_initial.xlsx'  # 输入文件路径
n = 4  # 每个动作重复次数

# 调用函数生成新的动作表格
new_action_table = generate_obj_one_action_table(file_path, n)
print(f"Generated table: {new_action_table}")
