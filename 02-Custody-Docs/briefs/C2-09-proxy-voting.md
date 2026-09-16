# C2-09 — Proxy services: voting, general meetings, shareholder-related services — BRIEF
> **Category:** C2 — Core Business Flows · **Difficulty:** ◑ · **Banking-relevant:** 💳

> **One-liner:** Proxy services enable a custodian or asset manager to vote shares on behalf of clients, participate in meetings, and report shareholder-related events.

> **Why an enterprise architect / trainee cares:** Proxy is a high-stakes, high-visibility corporate action task. A lost vote on a contentious issue (e.g., a contested election) creates a compliance and reputation event.

## Quick definition
Proxy services are the set of operations through which a custodian or agent votes shares, attends shareholder meetings, and manages shareholder data related to corporate actions.

## Key ideas / terms
- **Proxy:** A vote cast on behalf of a shareholder by a delegate (e.g., custodian, fund manager, or agent) due to the shareholder being unable to vote directly.
- **Proxy voting:** The actual act of voting using a proxy.
- **Proxy solicitation:** The act of soliciting a client’s vote assertion (e.g., a proxy letter or electronic approval).
- **Proxy instruction:** The client’s direction to vote or delegate.
- **General meeting / annual meeting:** The forum where shareholders vote.
- **Proxy statement:** The document that contains voting instructions and meeting details.
- **Cut-off / deadline / stop / close:** The last time to accept proxy instructions.
- **Time / date / time**: The specific time a meeting starts.
- **Method / voting: paper / electronic / in-person / 0neline; On-line / Friday / weekend / Tuesday / Wednesday / Thursday / Saturday / Sunday**: The preferred proxy voting method.
- **Voter / proxy**: The delegate who receives the proxy.
- **Release / surrender / keep-physical**: The legal act of giving up a stock.
- **Introduction / both / dual / formal / informal / fodder / needs**: A list of different categories of shareholders (e.g., institutional, beneficial owner, physical).
- **Trustee / corporate / large / trust / client / document / set**: The entity that holds the shares.
- **A-1 / A-2 / B-1 / 2 / 3 / 4 / 5**: Shareholder class identifiers.
- **European / European / extra-European / non-European / home**: The area / political / Crypto / crypto.
- **National / national / local / Foreign**: The jurisdiction.
- **Self-proxy**: A proxy that contains an election by the client directly.

## Differences
The following terms are related to proxy services. They are not identical and should not be confused:

- **Proxy voting vs proxy solicitation.**
- **Proxy services vs proxy agent.**
- **Proxy vs proxy statement.**
- **Proxy vs proxy vote vs proxy solicitation.**
- **Proxy vote vs proxy vote row.**
- **Proxy vote vs proxy solicitation.**
- **Proxy vote vs proxy vote row.**
- **Proxy vote vs proxy vote row.**
- **Proxy vote vs proxy vote row.**
- **Proxy vote vs proxy vote row.**

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,stroke-width:1px,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:1px,color:#000
    A[Proxy solicitation]:::critical --> B{Client instruction}:::ok
    B -->|Yes| C[Vote delegation]:::core
    B -->|No| D[Vote withheld]:::critical
    C --> E[Vote]:::critical
    E --> F[Meeting / report]:::core
    D --> G[No vote]:::context
    style A critical
    style B ok
    style C core
    style D risk
    style E critical
    style F core
    style G context
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,stroke-width:1px,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:1px,color:#000
    class A critical
    classB ok
    classC core
    classD risk
    classE critical
    classF core
    classG context
```

## When to use / when NOT to use
- ✅ **Use when:** The client has shares that require voting; the bank has a valid proxy delegation.
- ⚠️ **Avoid when:** The proxy is not authenticated; the client has been instructed to abstain; the meeting deadline has passed.

## Banking 💳 example
A major pension fund holds shares in a US corporation through a global custodian. The custodian:
1. Receives a proxy solicitation from the US issuer.
2. Ingests the proxy ballot and shares the instruction to the pension fund’s investment manager.
3. The investment manager instructs the custodian to vote.
4. The custodian votes as directed.
5. The custodian reports the vote to the investor and the issuer.

If the custodian fails to vote, the proxy company reports a non-participation, and the fund’s vote is not registered, potentially invalidating a contested result.

## Common confusions (don’t mix these up)
- **Proxy vs proxy vote**: Proxy is the voting authority; proxy vote is the actual ballot.
- **Proxy vs proxy solicitation**: Proxy is the authority; solicitation is the request.
- **Proxy vs proxy statement**: Proxy is the authority; statement is the document.

## Interview / recall prompt
“Explain proxy services in 2 minutes without notes.” → Hit: proxy solicitation, instruction, deadline, vote, non-participation, issuer, regulator, proxy copy.

## Status
☐ Not started · See detail doc: `details/C2-09-proxy-voting.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
