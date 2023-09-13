This spec roughly describes the python implementation of PLONK protocol in [proof-system-repo](https://github.com/stechu/proof-systems)
## Constraint System

The constraint system $\mathcal{C} = (\mathcal{V}, \mathcal{Q})$ can be defined as:
* wire vector $\vec{x} \in \mathbb{F}^m$, where $\vec{x}[:\ell]$ is public input, and $\vec{x}[\ell:]$ is witness        
* $\mathcal{V} = (\vec{a}, \vec{b}, \vec{c})$, where $\vec{a}, \vec{b}, \vec{c} \in [m]^n$. We think of $\vec{a}, \vec{b}, \vec{c}$ as the left, right, and output sequence of $\mathcal{C}$. For example, we can think $a_i$ (where $i \in [n]$) is the index to $\vec{x}$ 
* $\mathcal{Q} = (\vec{q_L}, \vec{q_R}, \vec{q_O}, \vec{q_M}, \vec{q_C}) \in (\mathbb{F}^n)^5$ where $\vec{q_L}, \vec{q_R}, \vec{q_O}, \vec{q_M}, \vec{q_C}$ are "selector vectors"

We say $\vec{x}$ satisfies $\mathcal{C}$ if for each $i \in [n]$,
$$(\vec{q_L})_i \cdot (\vec{x})_{a_i} + (\vec{q_R})_i \cdot (\vec{x})_{b_i} + (\vec{q_O}_i) \cdot (\vec{x})_{c_i} + (\vec{q_M})_i \cdot (\vec{x})_{a_i} \cdot (\vec{x})_{b_i} + (\vec{q_C})_i = 0$$

Sometimes we say $(x, w)$ satisfies $\mathcal{C}$ where $x = \vec{x}[:\ell] \in \mathbb{F}^{\ell}$ and $w=\vec{x}[\ell:] \in \mathbb{F}^{m-\ell}$

## High Level Protocol
### Prepare

^prepare

Suppose $\mathcal{V} = (\vec{a}, \vec{b}, \vec{c})$, think $\mathcal{V}$ as a single vector $V \in [m]^{3n}$. For $i \in [m]$, let $T_i \subset [3n]$ be the set of indices $j\in [3n]$ such that $V_j = i$, Now we define a partition $\mathcal{T}_{\mathcal{C}}$ of $V$:
$$\mathcal{T}_{\mathcal{C}} := \{T_i\}_{i \in [m]}$$
Now we can define a permutation $\sigma(\mathcal{T})$ that is used to check all values within a single partition is equal. We just need for each partition $T_i$, $\sigma(\mathcal{T})$ contains a cycle (or really just need a spanning tree) going over all elements of $T_i$ . We say $f_1, \ldots, f_k$ **copy satisfies** $\mathcal{T}$, if after converting them to extended permutation polynomial, $f$, $(f(1), \ldots, f(kn)) \in \mathbb{F}^{kn}$, we have $f(\ell)=f(\ell')$ whenever $\ell$ and $\ell'$ belong to the same partition of $\mathcal{T}$ (details in [[Permutation Check]]).
###  Protocol
1. Let $\vec{x}$ be prover's witness assignment that consistent with the public input, prover computes three polynomials $A, B, C \in \mathbb{F}_{<n}[X]$ , where for $i \in [n]$
$$ A(g^i) = (\vec{x})_{a_i}, B(g^i)=(\vec{x})_{b_i}, C(g^i)=(\vec{x})_{c_i}$$
2. Prover and Verifier run the extended permutation check protocol using the permutation $\sigma$ between $(A, B, C)$ and itself.  As described in [[#^prepare]] , this checks whether $(A, B, C)$ copy satisfies $\mathcal{T}_{\mathcal{C}}$
3. Prover computes the "Public input polynomial"
$$PI(X) := \sum_{i\in [\ell]} - \vec{x}_i \cdot L_i(X)$$
4. Verifier checks the identity
$$q_L \cdot A + q_R \cdot B + q_O \cdot C + q_M \cdot A \cdot B + (q_C + PI) = 0$$ on $H=\{1, \omega, \omega^2, \ldots, \omega^{n-1}\}$

## Protocol Implementation

A circuit is uniquely defined by the following polynomials and the integer $n$:
- $q_M(X), q_L(X), q_R(X), q_O(X), q_C(X)$, the `selector` polynomials
- $S_{ID_1}(X) = X$, $S_{ID_2}(X)=k_1 X$, $S_{ID_3} = k_2 X$: the identity permutation applied to $\vec{a}, \vec{b}, \vec{c}$. $k_1, k_2 \in F$ are chosen such that $H$, $k_1 \cdot H$, $k_2 \cdot H$ are distinct cosets of $H$ in $\mathbb{F}*$
- We can denote $H':= H \cup (k_1 \cdot H) \cup (k_2 \cdot H)$, let $\sigma: [3n] \rightarrow [3n]$ be a permutation:
$$\sigma(i) = \cases{
    & $x=\omega^i$ \cr
   0  & $x \in H \land x \neq \mathbb{g}^i$
   }$$