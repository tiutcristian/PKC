# Factoring 7531 using the Continued Fractions Method

Find a non-trivial factor of $N = 7531$ using the continued fractions method.

## 1) Continued fraction of $\sqrt{7531}$

First, $a_0 = \lfloor\sqrt{7531}\rfloor = 86$ because $86^2=7396$ and $87^2=7569$.

We use the standard recurrence for the continued fraction of $\sqrt{N}$:

- Initialize: $m_0=0$, $d_0=1$, $a_0=\lfloor\sqrt{N}\rfloor$.
- For $k\ge 0$:
$m_{k+1} = d_k a_k - m_k,\qquad d_{k+1} = \frac{N - m_{k+1}^2}{d_k},\qquad a_{k+1} = \left\lfloor\frac{a_0 + m_{k+1}}{d_{k+1}}\right\rfloor.$

The first few triplets $(m_k,d_k,a_k)$ are:

| $k$ | $m_k$ | $d_k$ | $a_k$ |
|---:|---:|---:|---:|
| 0 | 0  | 1   | 86 |
| 1 | 86 | 135 | 1  |
| 2 | 49 | 38  | 3  |
| 3 | 65 | 87  | 1  |
| 4 | 22 | 81  | 1  |
| 5 | 59 | 50  | 2  |

So the continued fraction begins:
$\sqrt{7531} = [86; 1, 3, 1, 1, 2, \dots]$

---

## 2) Convergents and the $r_k$ values

Convergents are computed from partial quotients $a_k$ using:

- $p_{-2}=0$, $p_{-1}=1$; $q_{-2}=1$, $q_{-1}=0$
- $p_k = a_k p_{k-1} + p_{k-2},\qquad q_k = a_k q_{k-1} + q_{k-2}.$

Then compute $r_k = p_k^2 - N q_k^2$.

| k | $a_k$ | $p_k$ | $q_k$ | $r_k = p_k^2 − 7531 q_k^2$ |
|---:|---:|---:|---:|---:|
| 0 | 86 | 86  | 1 | -135 |
| 1 | 1  | 87  | 1 | 38 |
| 2 | 3  | 347 | 4 | -87 |
| 3 | 1  | 434 | 5 | **81** |
| 4 | 1  | 781 | 9 | -50 |
| 5 | 2  | 1996| 23| 117 |

At $k = 3$ we get a perfect square immediately:  
$p_3 = 434,\quad q_3 = 5$  
$r_3 = 434^2 - 7531\cdot 5^2 = 188356 - 188275 = 81 = 9^2.$

---

## 3) Congruence of squares and extracting a factor

From $r_3 = p_3^2 - N q_3^2$ we rearrange:  
$p_3^2 - 9^2 = N\cdot q_3^2 = 7531\cdot 25.$  

Therefore, $434^2 \equiv 9^2 \pmod{7531}.$

So $7531$ divides $(434-9)(434+9)$:  
$(434-9)(434+9)=425\cdot 443.$

Now compute gcds:

### I. $\gcd(434-9, 7531)=\gcd(425,7531)$

Euclid steps:

| step | $a$ | $b$ | $a = b \cdot q + r$ |
|---:|---:|---:|---|
| 1 | 7531 | 425 | 7531 = 425·17 + 306 |
| 2 | 425 | 306 | 425 = 306·1 + 119 |
| 3 | 306 | 119 | 306 = 119·2 + 68 |
| 4 | 119 | 68  | 119 = 68·1 + 51 |
| 5 | 68  | 51  | 68 = 51·1 + 17 |
| 6 | 51  | 17  | 51 = 17·3 + 0 |

Hence,
$\gcd(425,7531)=17.$

### II. $\gcd(434+9, 7531)=\gcd(443,7531)$

Since
$7531 = 443\cdot 17,$
we have
$\gcd(443,7531)=443.$

---

## Result
We found non-trivial factors of $7531$:  
$7531 = 17\cdot 443.$

---

For this particular $N$, the relation at $k = 3$ already yields a square ($81$), so the usual
“combine several relations to make a square” step is not needed.
