directory="/Users/admin/Desktop"

#  根据正则表达式查询文件名
files=$(find "$directory" -type f -regex '.*工作内容-[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}\.txt')
old_filename=${files[@]}


today=$(date +%Y-%m-%d)
new_filename="${directory}/${today}.txt"
# echo $today

# 判断文件是否存在
if [[ -f "$old_filename" ]]; then
  # 重命名文件
  mv "$old_filename" "$new_filename"
  echo "文件已重命名为 $new_filename"
else
  echo "文件 $old_filename 不存在"
fi