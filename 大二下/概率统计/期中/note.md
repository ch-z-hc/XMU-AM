## 指数分布

$$
f(x)=
\begin{cases}
\lambda e^{-\lambda x}, & x \ge 0 \\
0, & x < 0
\end{cases}
\\
F(x)=P(X\le x)=1-e^{-\lambda x},\quad x\ge 0 \\
E(X)=\frac{1}{\lambda} \\
D(X)=\frac{1}{\lambda^2}
$$

## 均匀分布

$$
f(x)=
\begin{cases}
\dfrac{1}{b-a}, & a\le x\le b \\
0, & \text{Otherwise}
\end{cases}
\\
F(x)=P(X\le x)=
\begin{cases}
0, & x<a \\
\dfrac{x-a}{b-a}, & a\le x\le b \\
1, & x>b
\end{cases}
\\
E(X)=\dfrac{a+b}{2}
\\
D(X)=\frac{(b-a)^2}{12}
$$

## 正态分布
$$
X\sim N(\mu,\sigma^2)
\\
f(x)=
\dfrac{1}{\sigma\sqrt{2\pi}}
e^{-\dfrac{(x-\mu)^2}{2\sigma^2}},
\\
F(x)=
\Phi\left(\frac{x-\mu}{\sigma}\right)
\\
\Phi(x) =
\int_{-\infty}^{x}
\dfrac{1}{\sqrt{2\pi}}
e^{-\dfrac{t^2}{2}}
\mathrm dt
\\
E(X)=\mu
\\
D(X)=\sigma^2
$$

## 泊松分布

$$
X\sim P(\lambda),\quad \lambda>0
\\
P(X=k)=
\dfrac{\lambda^k e^{-\lambda}}{k!},
\quad k=0,1,2,\dots
\\
F(k)=P(X\le k)=
\sum_{i=0}^{k}
\dfrac{\lambda^i e^{-\lambda}}{i!},
\quad k=0,1,2,\dots
\\
E(X)=\lambda
\\
D(X)=\lambda
$$

## 二项分布

伯努利分布：即 $n=1$ 的二项分布。
$$
E(X) = np \\
D(X) = np(1-p)
$$
