<!--
  Symbiote-black / crimson Spider-Man theme.

  Regenerate the art assets:
    python3 scripts/make_banner.py         -> web-banner.svg    (header: webbing, name, symbiote drip)
    python3 scripts/make_spider_svg.py    -> spider-ascii.svg  (ASCII spider, web-weave animation)
    python3 scripts/make_info_card.py     -> info-card.svg     (neofetch panel)
    python3 scripts/make_divider.py       -> web-divider.svg   (section rule)

  Palette: bg #0a0a0a · crimson #E62429 · fire #FF3B30 · bone #EDEDED · web #3A3F44
-->

<div align="center">

<img src="./web-banner.svg" width="100%" alt="HariCipher — SOC · DFIR · Detection Engineering" />

<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=21&duration=3200&pause=900&color=E62429&center=true&vCenter=true&width=640&lines=friendly+neighbourhood+SOC+analyst;with+great+power+comes+great+responsibility;SIEM+%7C+Threat+Hunting+%7C+Detection+Engineering;my+spider-sense+pinged+on+event+4104" alt="Typing SVG" /></a>

<img src="./web-divider.svg" width="100%" alt="" />

<h3><code>HariCipher@web ~ $ whoami</code></h3>

<table>
<tr>
<td valign="top"><img src="./spider-ascii.svg" width="330" alt="HariCipher — ASCII spider" /></td>
<td valign="top"><img src="./info-card.svg" width="500" alt="HariCipher — role, stack, focus" /></td>
</tr>
</table>

<p>
3rd-year CS student who spends his nights in Splunk instead of on rooftops.<br/>
Four months in a real SOC pulling apart <b>Bandook RAT</b> and <b>TrickBot</b> traffic, writing the
detections nobody else wanted to tune, and learning that the alert everybody ignores is the one that matters.
</p>

<img src="./web-divider.svg" width="100%" alt="" />

<h3><code>HariCipher@web ~ $ arsenal</code></h3>

![Splunk](https://img.shields.io/badge/Splunk-0a0a0a?style=for-the-badge&logo=splunk&logoColor=E62429&labelColor=0a0a0a) ![Wazuh](https://img.shields.io/badge/Wazuh-0a0a0a?style=for-the-badge&labelColor=0a0a0a) ![Wireshark](https://img.shields.io/badge/Wireshark-0a0a0a?style=for-the-badge&logo=wireshark&logoColor=E62429&labelColor=0a0a0a) ![tshark](https://img.shields.io/badge/tshark-0a0a0a?style=for-the-badge&logo=wireshark&logoColor=E62429&labelColor=0a0a0a)

![Python](https://img.shields.io/badge/Python-0a0a0a?style=for-the-badge&logo=python&logoColor=E62429&labelColor=0a0a0a) ![Bash](https://img.shields.io/badge/Bash-0a0a0a?style=for-the-badge&logo=gnubash&logoColor=E62429&labelColor=0a0a0a) ![Kali](https://img.shields.io/badge/Kali_Linux-0a0a0a?style=for-the-badge&logo=kalilinux&logoColor=E62429&labelColor=0a0a0a) ![EVTX](https://img.shields.io/badge/Windows_EVTX-0a0a0a?style=for-the-badge&labelColor=0a0a0a)

![MITRE](https://img.shields.io/badge/MITRE_ATT%26CK-0a0a0a?style=for-the-badge&labelColor=0a0a0a) ![Shuffle](https://img.shields.io/badge/Shuffle_SOAR-0a0a0a?style=for-the-badge&logo=zapier&logoColor=E62429&labelColor=0a0a0a) ![OpenCanary](https://img.shields.io/badge/OpenCanary-0a0a0a?style=for-the-badge&logo=hackthebox&logoColor=E62429&labelColor=0a0a0a) ![VMware](https://img.shields.io/badge/VMware-0a0a0a?style=for-the-badge&logo=vmware&logoColor=E62429&labelColor=0a0a0a)

<img src="./web-divider.svg" width="100%" alt="" />

<h3><code>HariCipher@web ~ $ cat case-files/*</code></h3>

</div>

> ### `CASE-001` · TRACEX — Windows Event Log Analyzer
> **Caught in the web:** a false positive nobody had noticed — service account noise firing a
> privilege-escalation rule. Found it, fixed it, kept the detection.
>
> Cross-platform EVTX analyser in Python with 5 correlated rules (brute force, LOLBin execution,
> privilege-escalation sequencing, alternate credential use, account modification), tested against
> **28,000+ real events** on Windows 11 and Kali. Confidence scoring, MITRE ATT&CK mapping, SQLite
> persistence, interactive HTML dashboard — **no SIEM required**.
>
> [`→ HariCipher/tracex`](https://github.com/HariCipher/tracex)

> ### `CASE-002` · Bandook RAT — C2 Traffic Analysis
> **Caught in the web:** dual C2 infrastructure that DNS-only monitoring missed entirely — a
> hardcoded IP reached out **37 minutes before any DNS activity**.
>
> Full IOC extraction and ATT&CK mapping across `T1071`, `T1571`, `T1573`, `T1568`.
>
> [`→ HariCipher/bandook-c2-traffic-analysis`](https://github.com/HariCipher/bandook-c2-traffic-analysis)

> ### `CASE-003` · Home SOC Lab
> **Caught in the web:** a real SSH credential attempt against the honeypot — logged, detected,
> and written up end to end.
>
> Splunk + Wazuh SOC lab on Kali and VMware Workstation, with an OpenCanary honeypot in a
> segmented DMZ isolated via `iptables` (TCP 6591). Detections built for brute force and
> lateral movement.
>
> [`→ HariCipher/Home-Soc-Lab`](https://github.com/HariCipher/Home-Soc-Lab)

> ### `CASE-004` · Splunk Detection Engineering
> **Caught in the web:** PowerShell execution, failed auth, account creation and service
> installation — all validated against real Windows telemetry, not synthetic samples.
>
> Documented SPL queries with MITRE mapping for every rule.
>
> [`→ HariCipher/Splunk-Detection-engineering`](https://github.com/HariCipher/Splunk-Detection-engineering)

<div align="center">

<img src="./web-divider.svg" width="100%" alt="" />

<h3><code>HariCipher@web ~ $ tail -f the-web-of-signals</code></h3>

<img height="180em" src="https://github-stats-extended.vercel.app/api?username=HariCipher&show_icons=true&theme=dark&hide_border=true&bg_color=0A0A0A&title_color=E62429&icon_color=FF3B30&text_color=EDEDED"/>
<img height="180em" src="https://github-readme-stats-nu-indol-97.vercel.app/api/top-langs/?username=HariCipher&layout=compact&theme=dark&hide_border=true&bg_color=0A0A0A&title_color=E62429&text_color=EDEDED"/>

<br/>

<img src="https://github-readme-streak-stats-fhfiap706-chiefgyk3ds-projects.vercel.app/api?user=HariCipher&hide_border=true&background=0A0A0A&border=2A2A2A&stroke=2A2A2A&ring=E62429&fire=FF3B30&currStreakNum=EDEDED&sideNums=EDEDED&currStreakLabel=E62429&sideLabels=6E7681&dates=6E7681"/>

<img src="./web-divider.svg" width="100%" alt="" />

<h3><code>HariCipher@web ~ $ cat threat-board</code></h3>

<table>
<tr>
<td><b>SOC Analyst Training</b><br/><sub>Gardiyan System Security Technologies · Turkey (remote)</sub></td>
<td align="right"><sub>Sep 2025 – Jan 2026</sub></td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/TryHackMe-0a0a0a?style=flat-square&logo=tryhackme&logoColor=E62429&labelColor=0a0a0a" alt="TryHackMe"/> <b>Hackfinity Battle CTF</b><br/><sub>Rank 265 · 600 pts</sub></td>
<td align="right"><sub>2025</sub></td>
</tr>
<tr>
<td><b>B.Tech, Computer Science Engineering</b><br/><sub>Poornima University, Jaipur</sub></td>
<td align="right"><sub>Expected 2028</sub></td>
</tr>
</table>

<img src="./web-divider.svg" width="100%" alt="" />

<h3><code>HariCipher@web ~ $ ls threads/</code></h3>

[![Portfolio](https://img.shields.io/badge/Portfolio-E62429?style=for-the-badge&logo=vercel&logoColor=EDEDED&labelColor=0a0a0a)](https://HariCipher.github.io)  [![Email](https://img.shields.io/badge/Email-E62429?style=for-the-badge&logo=gmail&logoColor=EDEDED&labelColor=0a0a0a)](mailto:thisisharilal@gmail.com) [![Discord](https://img.shields.io/badge/Discord-E62429?style=for-the-badge&logo=discord&logoColor=EDEDED&labelColor=0a0a0a)](https://discord.com/channels/@me)

<img src="./web-divider.svg" width="100%" alt="" />

<sub><i>with great logs comes great responsibility</i></sub>

</div>
