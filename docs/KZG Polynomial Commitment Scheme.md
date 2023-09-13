
## Polynomial Commitment Scheme

Prover commits to a polynomial $f(X)$ in $\mathbb{F}^{(\leq d)}_p[X]$  to $com_f$ ($d$, $com_f$, $u$, $v$ are public to both prover and verifier):
- **eval**: for public $u,v \in \mathbb{F}_p$, prover can convince the verifier that committed poly satisfies:
	$f(u) = v$ and $deg(f)\leq d$
- Eval proof size and verifier time should be $O_{\lambda}(\log d)$

## Pairing 

KZG requires a primitive on elliptic curves named **pairing**. Let $\mathbb{G}_1$ and $\mathbb{G_2}$ be two elliptic curves with a pairing $e: \mathbb{G_1} \times \mathbb{G_2} \rightarrow \mathbb{G}_T$ is a bilinear mapping between a pair of one element in $\mathbb{G}_1$, one element in $\mathbb{G}_2$, to an element in a "target" group $\mathbb{G}_T$. Bilinear means:

$$ e(P, Q+R) = e(P, Q) \, e(P, R)$$$$e(P+S, Q) = e(P, Q) \, e(S, R) $$
More can be found in [Vitalik's blog post](https://vitalik.ca/general/2017/01/14/exploring_ecp.html).

## KZG 

Group $\mathbb{G}_1 :=\{ 0, G, 2\,G, 3\,G, \ldots, (p-1)\,G\}$ of order $p$, and $\mathbb{G}_2 := \{0, H, 2\, H, 3\,H, \ldots, (q-1) \,H \}$ of order q,  Group $\mathbb{G}_T :=\{ 0, T, 2\,T, 3\,T, \ldots, (r-1)\,T\}$ of order $r$, a pairing $e: \mathbb{G_1} \times \mathbb{G_2} \rightarrow \mathbb{G}_T$ 

>[!scheme] KZG Setup and Commit
> $\texttt{setup}(\lambda) \rightarrow (gp, hq)$
> - sample random $\tau \in \mathbb{F}_p$
> - $gp = ( H_0 = G, H_i = \tau \, G, H_2 = \tau^2 \, G, \ldots, H-d = \tau^{d} \, G) \in \mathbb{G}^{d+1}$
> - $hq = ( I_0 = H, I_2 = \tau \, H)$
> - delete $\tau$ (trusted setup)
> 
> $\texttt{commit}(gp, f) \rightarrow com_f$, where $com_f := f(\tau) G \in \mathbb{G}$
> - Suppose $f(X) = f_0 + f_1 X + \ldots + f_d X^d$
> - $com_f = f_0 H_0 + \ldots + f_d H_d =f(\tau) G$

Now let's look at how does verifier can verify the $f(u) =v$ given $com_f, u, v$. Let's define a new poly $\hat{f}$ as $\hat{f} = f -v$. Since we know $f(u) - v = 0$, then $\hat{f}(u) = 0$, essentially this says $u$ is a root of $\hat{f}$ or $(X - u)$ divides $\hat{f}$. Which is equivalent to the following statement:

$$\exists q \in \mathbb{F}_p[X] \; s.t. \; q(X) \cdot (X-u) = f(X) - v = \hat{f}$$
We call $q(X)$ a **quotient polynomial**.  Now we can construct KZG prove and verify algorithm.

>[!scheme] KZG Prove and Verify
>$\texttt{Prove}(gp, f, u, v) \rightarrow com_q$
>- compute $com_q = q(\tau) G$ 
>
>$\texttt{Verify}(gp, com_q, u, v) \rightarrow \{0, 1\}$
>- check $q(\tau) \cdot (\tau - u ) \, T = (f(\tau)  - v) \, T$  
>- we can see the RHS  is $e((com_f \,  - v)\, G, H)$
>- we can see the LHS is $e(com_q \, G, (I_1 - u \, H))$

Essentially, the prover send the commitment, $com_q$,  the quotient polynomial evaluated at the secret point $\tau$, which can be viewed as a commitment of the quotient polynomial to the verifier.  Now, we need to check the validity of the quotient polynomial. The intuition is that it is hard to find a "fake" quotient polynomial if you don't know the evaluation point. Remember the statement where we define polynomial, the verifier essentially need to check:
$$q(\tau) \cdot (\tau - u ) = (f(\tau)  - v)$$
However, the verifier doesn't know $\tau$, so instead, the verifier need to check the equation using $(gp, hq)$, which she does know. And that's exactly where we use the bilinear property of pairing: the verifier knows $com_q=q(\tau) \, G$, $com_f=p(\tau) \, G$, $u$, $v$, thus it is sufficient to perform the checking in the $\texttt{verify}$.


