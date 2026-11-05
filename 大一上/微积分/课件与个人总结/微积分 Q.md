# 微积分

## Q 1 脑瘫 or 记！

$$
\tan 'x = \frac{1}{\cos^2 x} \\
d \tan x = \frac{1}{\cos^2 x} dx \\
\int \tan x dx = \int \frac{\sin x}{\cos x} dx = - \int \frac{1}{\cos x} d \cos x = - \ln |\cos x| + C \\
\int \cot x dx = \int \frac{\cos x}{\sin x} dx = \int \frac{1}{\sin x} d \sin x = \ln |\sin x| + C \\
\int \sec x dx= \int \frac{1}{\cos x} dx = \int \frac{\cos x}{\cos^2 x} dx = \int \frac{d \sin x}{1 - \sin^2 x} = \\ 
\frac{1}{2} \int \left( \frac{1}{1-\sin x} + \frac{1}{1+\sin x}\right) d \sin x = \frac{1}{2} \left(-\ln |1-\sin x| + \ln |1+\sin x| \right) + C \\
=\frac{1}{2} \ln \left |\frac{1+ \sin x}{1 - \sin x} \right| +C = =\frac{1}{2} \ln \left |\frac{(\sin x + 1)^2}{\cos^2 x} \right| +C  = \ln \left | \sec x + \tan x \right | + C \\
\int \csc x dx= \int \frac{1}{\sin x} dx = \int \frac{\sin x}{\sin^2 x} dx = -\int \frac{d \cos x}{1 - \cos^2 x} = \\ 
-\frac{1}{2} \int \left( \frac{1}{1-\cos x} + \frac{1}{1+\cos x}\right) d \cos x = -\frac{1}{2} \left(-\ln |1-\cos x| + \ln |1+\cos x| \right) + C \\
=\frac{1}{2} \ln \left |\frac{1 - \cos x}{1 + \cos x} \right| +C = =\frac{1}{2} \ln \left |\frac{(1- \cos x)^2}{\sin^2 x} \right| +C  = \ln \left | \csc x - \cot x \right | + C
$$

旋转，绕 $x / y$ 轴？

## Q 2 万能代换

$$
t = \tan\frac{x}{2} \\
\sin x = \frac{2t}{t^2 + 1} \\
\cos x = \frac{1 - t^2}{t^2 + 1} \\
dx = \frac{2}{1 + t^2} dt
$$

## Q 3 三角函数定积分相关结论

$$
\int _0^\frac{\pi}{2} f(\sin  x) dx = \int _0^\frac{\pi}{2} f(\cos  x) dx \\
\int _0^\pi x f(\sin  x) dx = \frac{\pi}{2}\int _0^\pi f(\sin  x) dx= \pi\int _0^\frac{\pi}{2} f(\sin  x) dx \\
\int_0^\frac{\pi}{2} x \left( f(\sin x) + f(\cos x) \right) dx= \frac{\pi}{2} \int_0^{\frac{\pi}{2}} f(\sin x) dx
$$

## Q 4 含 $e^x$

$$
\int \frac{1}{1 + e^x} dx = \int \frac{1 + e^x - e^x}{1 + e^x} dx = \int \left(1 - \frac{e^x}{1 + e^x}\right) dx
$$

## Q 5 三角函数不定积分

遇到形如：
$$
\int \left( \sin (\ln x) + \cos (\ln x) \right) dx
$$
把其中一个用分部积分展开可能可以消掉另外一个。



## Q 6 变限积分函数的求导

$$
F(x) = \int _{g(x)} ^ {h(x)} f(t) dt \\
F'(x) = f[h(x)] h'(x) - f[g(x)]g'(x)
$$

若 $f(t)$ 中含 $x$，由于积分变量为 $t$，因此能分离 $x$ 时直接分离即可。

否则，通过换元法将 $x$ 分离出来（换元时积分上下限也要换）。



## Q 7 弧长

$$
ds = \sqrt{(dx)^2 + (dy)^2} = \sqrt{1 + y'^2} dx
$$

若 $x, y$ 为 $t$ 的参数方程，即
$$
x = \varphi(t) \\
y = \phi(t)
$$
则：
$$
ds = \sqrt{(dx)^2 + (dy)^2} = \sqrt{\varphi'^2(t) + \phi'^2(t) } dt
$$
转换到极坐标，有： 
$$
x = \rho(\theta) \cdot \cos \theta \\
y = \rho(\theta) \cdot \sin \theta \\
ds = \sqrt{\rho^2(\theta) + \rho'^2(\theta)} d\theta
$$



## Q 8 常见泰勒展开

$$
e^x = 1 + x + \frac{1}{2 !} x^2 + \frac{1}{3!}x^3 + \cdots
$$

## Q 9 反三角函数求导

$$
\arctan' x = \frac{1}{x^2 + 1} \\
\arcsin' x = \frac{1}{\sqrt{1 - x^2}} \\
\arccos' x = - \frac{1}{\sqrt{1 - x^2}}
$$

## Q 10 替换

$$
1 + x^2 \overset{x = \tan u}{\longrightarrow} \sec u
$$



## Q 11 定积分 / 不定积分 换元 单调要求

定积分中不需要换元单调，但需要保证函数连续。

不定积分中换元需要单调，因为需要存在反函数使得换元变量可以回代。



## Q 12 三角函数换元 绝对值问题

不定积分中换元，需要满足两个条件：

1、单调；

2、值域相同。
$$
x = \sin t , t \in [-\frac{\pi}{2}, \frac{\pi}{2}], \cos t > 0 \\
x = \cos t, t \in [0, \pi], \sin t > 0 \\
x = \tan t, t \in [-\frac{\pi}{2}, \frac{\pi}{2}], \sec t > 0 \\
$$
当令 $x = \sec t$ 时，需要讨论，因为包含完整 $\sec t$ 值域的区间无法使得 $\tan t > 0$。



## Q 13 拉格朗日中值定理

$$
\exist c \in (a, b),  f'(c) = \frac{f(a) - f(b)}{a - b}
$$

## Q 14 拆！

被积函数不是奇函数 / 偶函数，但是可以拆成奇函数 / 偶函数 + 简单函数的形式。



## Q 15 $\lim \sum \to \int$

先考察积分上限为 $1$，下限为 $0$ 的情况：
$$
\frac{1}{n} \to dx \\
\frac{i}{n} \to x \\
\text {e.x. } \lim_{n \to \infty} \sum_{i=1}^n \frac{1}{n} \frac{i}{n} \sqrt{1 + \left( \frac{i}{n}\right)^2} = \int_0^1 x \sqrt{1 + x^2} dx
$$
其他情况观察上下限，得出类似结论。



## Q 16 $f(x) = g(x) + \int_a^b t(c)f(c)dc$

把 $\int_a^b t(c)dc$ 写成常数 $C$ 的形式再嵌套一层 $C = ?$ 即可求出 $C$。



## Q 17 简单多项式的分式函数

不要再换了，除除肯定能得到答案。



## Q 18 三角函数带根号

考虑升幂，可能可以把根号搞掉。

