# 1. 修改输入数据格式

Model.py中定义了输入文件的格式。其中，源程序的输入包含三个文件（猜想）：
1. delay_file: 包含TAS的时间信息
2. spectra_file: 包含TAS的光谱信息
3. lambdas_file: 包含TAS的波长信息

现需要将csv文件的信息分别输入到源程序中的相应位置中。

# 2. 使用test_Model.py进行单元测试 

# 3. 修改findBordersbyCSV使其输出正确的范围
# 4. 修改Model.py 66行，使其切片正确的范围