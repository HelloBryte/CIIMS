"""
插入示例物品数据到 items 表
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_connection

def insert_sample_items():
    """插入示例物品数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 示例物品数据
    sample_items = [
        # 图书类
        ("Python编程从入门到实践", "图书", 10, "Python学习经典教材"),
        ("Java核心技术", "图书", 8, "Java开发必备参考书"),
        ("数据结构与算法分析", "图书", 5, "计算机科学基础教材"),
        ("数据库系统概念", "图书", 6, "数据库理论教材"),
        ("计算机网络", "图书", 7, "网络技术教材"),
        
        # 电子设备类
        ("笔记本电脑", "电子设备", 3, "Dell XPS 15，高性能开发用"),
        ("投影仪", "电子设备", 5, "教室教学用投影设备"),
        ("无线鼠标", "电子设备", 15, "Logitech无线鼠标"),
        ("键盘", "电子设备", 12, "机械键盘，适合编程"),
        ("显示器", "电子设备", 4, "27寸4K显示器"),
        
        # 体育用品类
        ("篮球", "体育用品", 20, "标准7号篮球"),
        ("足球", "体育用品", 15, "标准5号足球"),
        ("羽毛球拍", "体育用品", 10, "YONEX羽毛球拍"),
        ("乒乓球拍", "体育用品", 25, "双面胶皮乒乓球拍"),
        ("跳绳", "体育用品", 30, "计数跳绳"),
        
        # 实验器材类
        ("显微镜", "实验器材", 8, "生物实验用显微镜"),
        ("天平", "实验器材", 6, "精密电子天平"),
        ("烧杯套装", "实验器材", 20, "化学实验用玻璃器皿"),
        ("试管架", "实验器材", 15, "实验室常用器材"),
        ("安全护目镜", "实验器材", 50, "实验安全防护用品"),
        
        # 办公用品类
        ("A4打印纸", "办公用品", 100, "500张/包，白色A4纸"),
        ("订书机", "办公用品", 30, "标准订书机"),
        ("文件夹", "办公用品", 80, "A4文件夹，多种颜色"),
        ("计算器", "办公用品", 25, "科学计算器"),
        ("白板", "办公用品", 10, "可移动白板"),
    ]
    
    try:
        # 使用 INSERT IGNORE 避免重复插入
        sql = """
            INSERT INTO items (item_name, item_category, item_quantity, remark)
            VALUES (%s, %s, %s, %s)
        """
        
        cursor.executemany(sql, sample_items)
        conn.commit()
        
        print(f"成功插入 {len(sample_items)} 条物品数据！")
        
        # 显示插入的数据
        cursor.execute("SELECT item_id, item_name, item_category, item_quantity FROM items ORDER BY item_id")
        items = cursor.fetchall()
        print("\n当前 items 表中的数据：")
        print("-" * 80)
        print(f"{'ID':<5} {'物品名称':<25} {'类别':<15} {'库存':<10}")
        print("-" * 80)
        for item in items:
            print(f"{item[0]:<5} {item[1]:<25} {item[2]:<15} {item[3]:<10}")
        
    except Exception as e:
        print(f"插入数据时出错：{str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    insert_sample_items()

