"""
ModelName: CrawlingAcwingQuestionBank

Description: A Python script to crawl and download questions from the Acwing Question Bank website.

Author: Sanicee

LastEditDate: 2025-12-02

Input:
- Acwing.html (local HTML file of the Acwing Question Bank)

Output:
- Downloaded questions in a structured CSV file (e.g., acwing_problems.csv)

Flow:
1.Read & Parse: Read local Acwing.html file and parse HTML structure using BeautifulSoup (lxml).
2.Extract Lectures (L1): Locate and extract the Lecture Titles from class="panel-week" elements.
3.Extract Categories (L2): Access each lecture's content panel and extract Algorithm Categories from class="dayname".
4.Extract Problems (L3): Extract Problem Names from the class="clock-problem-title" links under each category.
5.Reorder & Output: Reverse the list of records ([Lecture, Category, Problem]) for chronological order, then write the final data to a CSV file using utf-8-sig encoding.
"""

import csv
from bs4 import BeautifulSoup
import os

def parse_acwing_html(html_file, output_csv):
    # 检查文件是否存在
    if not os.path.exists(html_file):
        print(f"错误：找不到文件 {html_file}")
        return

    print("正在读取 HTML 文件...")
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    results = []

    # 1. 查找所有的“讲” (Level 1)
    # 在HTML中，每一讲的标题在一个 id 为 week_xx 的 div 中
    lecture_headers = soup.find_all('div', class_='panel-week')

    for header in lecture_headers:
        # 获取第几讲的标题，例如 "第一讲 基础算法"
        lecture_title_tag = header.find('span', class_='week_title')
        if not lecture_title_tag:
            continue
        
        lecture_title = lecture_title_tag.get_text(strip=True)
        
        # 获取该header对应的 ID (例如 week_54)
        header_id = header.get('id')
        
        # 根据逻辑，内容区域的 ID 是 header ID 将 "week_" 替换为 "week_panel_"
        # 例如 week_54 -> week_panel_54
        if header_id:
            panel_id = header_id.replace('week_', 'week_panel_')
            content_panel = soup.find('div', id=panel_id)
            
            if content_panel:
                # 2. 查找算法类别 (Level 2)
                # 每一行包含一个算法类别和若干题目
                rows = content_panel.find_all('div', class_='row')
                
                for row in rows:
                    # 获取算法类别名称，例如 "快速排序"
                    category_tag = row.find('span', class_='dayname')
                    if category_tag:
                        category = category_tag.get_text(strip=True)
                        
                        # 3. 查找题目名称 (Level 3)
                        # 题目包含在 class 为 clock-problem-title 的 a 标签中
                        problem_links = row.find_all('a', class_='clock-problem-title')
                        
                        for link in problem_links:
                            # 题目文字在 span 标签内
                            problem_span = link.find('span')
                            if problem_span:
                                problem_name = problem_span.get_text(strip=True)
                                
                                # 将数据加入列表
                                results.append(["Advanced",lecture_title, category, problem_name])

    # HTML中是按时间倒序排列的（第六讲在前，第一讲在后）
    # 为了Notion打卡表好看，我们将其反转，变成第一讲在前
    results.reverse()

    # 写入 CSV
    print(f"正在写入 CSV 文件: {output_csv} ...")
    header = ['课程名称','第几讲', '算法类别', '题目名称']
    
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(results)

    print(f"完成！共提取了 {len(results)} 道题目。")

if __name__ == "__main__":
    # 输入文件名 (请确保该文件在同级目录下)
    input_file = 'AcwingAdvanced.html' 
    # 输出文件名
    output_file = 'Problems_Advanced.csv'
    
    parse_acwing_html(input_file, output_file)