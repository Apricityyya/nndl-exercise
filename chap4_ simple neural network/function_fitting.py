import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn

# ========== 1. 定义要拟合的函数 ==========
def target_function(x):
    """目标函数：sin(x)"""
    return np.sin(x)

# ========== 2. 生成训练和测试数据 ==========
np.random.seed(42)

# 训练集：随机采样 300 个点
x_train = np.random.uniform(-np.pi, np.pi, 300).reshape(-1, 1).astype(np.float32)
y_train = target_function(x_train).astype(np.float32)

# 测试集：均匀采样 100 个点
x_test = np.linspace(-np.pi, np.pi, 100).reshape(-1, 1).astype(np.float32)
y_test = target_function(x_test).astype(np.float32)

print(f"训练集形状: {x_train.shape}, 测试集形状: {x_test.shape}")

# ========== 3. 建立神经网络 ==========
class NeuralNet(nn.Module):
    def __init__(self):
        super(NeuralNet, self).__init__()
        # 第一层：1 输入 → 64 隐藏（ReLU）
        self.layer1 = nn.Linear(1, 64)
        # 第二层：64 隐藏 → 32 隐藏（ReLU）
        self.layer2 = nn.Linear(64, 32)
        # 输出层：32 隐藏 → 1 输出
        self.output = nn.Linear(32, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.output(x)
        return x

# ========== 4. 训练 ==========
model = NeuralNet()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.MSELoss()  # 均方误差

x_train_t = torch.tensor(x_train)
y_train_t = torch.tensor(y_train)
x_test_t = torch.tensor(x_test)
y_test_t = torch.tensor(y_test)

loss_history = []
for epoch in range(500):
    # 前向传播
    y_pred = model(x_train_t)
    loss = loss_fn(y_pred, y_train_t)
    
    # 反向传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    loss_history.append(loss.item())
    
    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch + 1}: Loss = {loss.item():.6f}")

# ========== 5. 测试 ==========
with torch.no_grad():
    y_pred_test = model(x_test_t).numpy()
    test_error = np.mean((y_pred_test - y_test) ** 2)
    print(f"\n测试集 MSE: {test_error:.6f}")

# ========== 6. 可视化 ==========
x_plot = x_test
y_true = target_function(x_plot)
y_pred = y_pred_test

plt.figure(figsize=(10, 5))
plt.plot(x_plot, y_true, 'b-', label='True function: sin(x)', linewidth=2)
plt.plot(x_plot, y_pred, 'r--', label='Neural Network fit', linewidth=2)
plt.scatter(x_train, y_train, alpha=0.3, s=20, label='Training data')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Function Fitting with ReLU Neural Network')
plt.grid()
plt.savefig('function_fit.png')
plt.show()