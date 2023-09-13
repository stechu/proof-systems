  
## Preliminaries and Notations 
- $n < d$, $n$ is the degree of the honest prover's polynomials, $d$ is the bound being enforced on malicious provers
- multiplicative subgroup $H \subset \mathbb{F}$ of order $n$ with generator $\mathbb{g}$ 
- for $i \in [n]$ , $L_i(X)$ is an element of $\mathbb{F}_{<n}[X]$ with:
   $$L_i(x) =  
   \cases{
   1 & $x=\mathbb{g}^i$ \cr
   0  & $x \in H \land x \neq \mathbb{g}^i$
   }$$
  then we note $\{L_i\}_{i \in [n]}$ is a Lagrange basis for $H$
- We denote the prover as $P_{poly}$, the verifier as $V_{poly}$, and trusted party as $\mathcal{I}$.

## Permutation Check

> Claim 1
> Fix $i \in [n]$, and $Z, Z* \in \mathbb{F}[X]$, then $L_i(a) (Z(a) - Z*(a)) = 0$ for each $a \in H$ if and only if $Z(\mathbb{g}^i) = Z*(\mathbb{g}^i)$

For $f,g \in \mathbb{F}_{<d}[X]$ and a permutation $\sigma : [n] \rightarrow [n]$ , we write $g = \sigma (f)$ if for each $i \in [n], g(\mathbb{g}^i) = f(\mathbb{g}^{\sigma(i)})$.  Now we show a ranged polynomial protocol enabling $P_{poly}$ (a.k.a. the prover) to prove that $g=\sigma(f)$.

**Preprocessed polynomials:** 
For each $i \in [n]$, we have 
- $S_{ID} \in \mathbb{F}_{<n}[X]$ defined by $S_{ID}(\mathbb{g}^i) = i$
- $S_{\sigma} \in \mathbb{F}_{<n}[X]$ defined by $S_\sigma(\mathbb{g}^i) = \sigma(i)$

**Inputs:**
- $f, g \in \mathbb{F}_{<n}[X]$

**Protocol:**
1. $V_{poly}$ chooses random $\beta, \gamma \in \mathbb{F}$  and sends them to $P_{poly}$
2. Let $f' := f + \beta \cdot S_{ID} + \gamma$  and $g' = g + \beta \cdot S_\sigma + \gamma$ . Thus, we have for $i \in [n]$:
   $$\begin{array}{l}
   f'(\mathbb{g}^i) = f(\mathbb{g}^i) + \beta \cdot i + \gamma \\
   g'(\mathbb{g}^i) = g(\mathbb{g}^i) + \beta \cdot \sigma(i) + \gamma \end{array}$$
3. $P_{poly}$  computes $Z \in \mathbb{F}_{<n}[X]$, such that $Z(\mathbb{g}) = 1$, and for $i \in \{2, \ldots, n\}$ 
 $$ Z(\mathbb{g}^i) = \prod_{1 \leq j < i}{f'(\mathbb{g}^j)/g'(\mathbb{g}^j)} $$
Note, $Z(\mathbb{g}^i) = Z(\mathbb{g}^{i-1}) f'(\mathbb{g}^{i-1})/ g'(\mathbb{g}^{i-1})$
if one of the product elements is undefined, which happens w.p. $negl(\lambda)$ over $\gamma$, the protocol is aborted. 
4.  $P_{poly}$ sends $Z$ to $\mathcal{I}$ 
5. $V_{poly}$ checks if for all $a \in H$
  - $L_1(a) (Z(a) - 1) = 0$
  - $Z(a) f'(a) = g'(a) Z(a \cdot \mathbb{g})$
  and output **acc** if all checks hold.

## Extended Permutation Check

We need to check a permutation across of the values of different polynomials. Suppose we have multiple polynomials $f_1, \ldots, f_k \in \mathbb{F}_{<d}[X]$ and a permutation $\sigma: [kn] \rightarrow [kn]$. For $(g_1, \ldots, g_k) \in (\mathbb{F}_{<d}[X])^k$, we say that $(g_1, \ldots, g_k) = \sigma(f_1, \ldots, f_k)$ if the following holds.

Define the sequences $(f_{(1)}, \ldots, f_{(kn)}), (g_{(1)}, \ldots, g_{(kn)}) \in \mathbb{F}^{kn}$ by
$$\begin{array}{l}
f_{((j-1) \cdot n + i)} := f_j(\mathbb{g}^i) \\
g_{((j-1) \cdot n + i)} := g_j(\mathbb{g}^i)\end{array}$$
for each $j \in [k], i \in [n]$. Then we have $g_{(l)} = f_{(\sigma(\ell))}$ for each $\ell \in [kn]$.

**Preprocessed Polynomials:** 
$S_{ID_1}, \ldots, S_{ID_k} \in \mathbb{F}_{<n}[X]$  defined by $S_{ID_j}(\mathbb{g}^i) = (j-1) \cdot n + i$ for each $i \in [n]$ . 

> In practice, only $S_{ID} = S_{ID_1}$ is actually included in the set of preprocessed polynomials, since all others can be computed: $S_{ID_j}(x) = S_{ID}(x) + (j-1) \cdot n$ 

For each $j \in [k]$, $S_{\sigma_j} \in \mathbb{F}_{<n}[X]$, defined by $S_{\sigma_j}(\mathbb{g}^i) = \sigma((j-1)\cdot n + i)$ for each $i \in [n]$. 

**Inputs:** 
$f_1, \ldots, f_k, g_1, \ldots, g_k \in \mathbb{F}_{<n}[X]$

**Protocol:**
1. $V_{poly}$ chooses random $\beta, \gamma \in \mathbb{F}$ and sends them to $P_{poly}$
2. Let $f'_j := f_j + \beta \cdot S_{ID_j} + \gamma$ and $g'_j := g_j + \beta \cdot S_{\sigma_j} + \gamma$ . So, we have, for $j \in [k], i \in [n]$,
 $$\begin{array}{l}
 f'_j(\mathbb{g}^i) = f_j(\mathbb{g}^i) + \beta \cdot ((j-1)\cdot n + i) + \gamma \\
 g'_j(\mathbb{g}^i) = g_j(\mathbb{g}^i) + \beta \cdot \sigma((j-1)\cdot n + i) + \gamma
  \end{array}$$
3. Define $f', g' \in \mathbb{F}_{<kn}[X]$ by 
$$\begin{array}{l} 
f'(X) := \prod_{j \in [k]}{f'_j(X)} \\
g'(X) := \prod_{j \in [k]}{g'_j(X)} \end{array}$$
4. $P_{poly}$ computes $Z \in \mathbb{F}_{<n}[X]$ , such that $Z(\mathbb{g}) = 1$, and for $i \in \{2, \ldots, n\}$
   $$ Z(\mathbb{g}^i) = \prod_{1\leq j < i}{f'(\mathbb{g}^j)/g'(\mathbb{g}^j)}$$
5. $P_{poly}$ sends $Z$ to $\mathcal{I}$
6. $V_{poly}$ checks for all $a \in H$
  - $L_1(a)(Z(a) - 1) = 0$
  - $Z(a)f'(a) = g'(a) Z(a \cdot g)$ 
  and output **acc** if and only if all checks hold.

## Using Permutation Check for Copy Constraints

Let $\mathcal{T} = \{T_1, \ldots, T_s\}$ be a partition of $[kn]$ into disjoint blocks. For $f_1, \ldots, f_k \in \mathbb{F}_{<n}[X]$, we say $f_1, \ldots, f_k$ copy satisfy $\mathcal{T}$ if $f_(\ell) = f(\ell')$ for any $\ell$ and $\ell'$ belong to the same block. For a set of copy constraints, define a partition of $\mathcal{T}$ to be the equivalent classes. Then define $\sigma (\mathcal{T})$ on $[kn]$ such that for each block $T_i \in \mathcal{T}$, $\sigma(\mathcal{T})$ contains a *cycle* going over all elements of $T_i$. Then, $(f_1, \ldots, f_k)$ copy-satisfy $\mathcal{T}$ if and only if $(f_1, \ldots, f_k) = \sigma(f_1, \ldots, f_k)$

