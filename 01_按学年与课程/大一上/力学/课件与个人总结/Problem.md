# Problem 1

![image-20241120180031824](C:\Users\chzhc\Nutstore\1\我的坚果云\总结\力学\pic\image-20241120180031824.png)

# Answer 1

以 $dz$ 的小圆盘为基本单元，绕 $z$ 轴的转动惯量为：
$$
I_z' = \frac{1}{2} r^2 dm
$$
由垂直轴定理：
$$
I_x' + I_y' = I_z' \\
$$
且由对称性可知：
$$
I_x' = I_y'
$$
因此可求：
$$
I_x' = \frac{1}{4}r^2 dm
$$

$$
I_z = \int_{-r}^r I_z' dz \\
I_x = \int_{-r}^rI_x'dz \\
I_x = I_y\\
dm = \lambda dz \\
\lambda = \frac{m}{2r}
$$

联立即可。
