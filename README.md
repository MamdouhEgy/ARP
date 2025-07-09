#  DDoS Detection in SDN using Entropy-Based Monitoring

This project (done during the M.Sc.) explores an **entropy-based method** for early detection and mitigation of **DDoS attacks** in Software-Defined Networks (SDN). Implemented using **Mininet**, **POX controller**, and custom packet generation via **Scapy**, it evaluates statistical randomness in destination IPs to identify abnormal behavior.

---

##  Project Overview

- **Institution**: TU Ilmenau – Communication Networks Group  
- **Author**: Mamdouh Muhammad  
- **Supervision**: Abdullah Soliman Alshra’a  
- **Toolset**: Mininet, POX, Scapy, sFlow-RT, Iperf  
- **Topology**: Fat-tree with 16 hosts and 4 OpenFlow switches  

---

##  Methodology

- **Entropy Measurement**:  
  Computes destination IP entropy in windows of 50, 300, or 500 packets  
- **Three Traffic Phases**:  
  1. Benign only (entropy ≈ 1.1)  
  2. Attack only (entropy ≈ 0.0)  
  3. Mixed traffic (entropy ≈ 0.5)  

- **Detection Logic**:  
  A DDoS is flagged if 5 consecutive windows fall below a computed entropy threshold  
- **Mitigation Strategy**:  
  Link bandwidth throttling using `TCLink` to disrupt attack traffic

---

##  Components

- `Topology.py`: Fat-tree topology with 80 hosts and dual controllers  
- `entropy.py`: Entropy-based anomaly detector integrated with POX  
- `Mamdouh Muhammad ARP Report.pdf`: Technical report  
- `Final Presentation - Mamdouh Muhammad - ARP.pptx`: Summary slides

---

##  Results Summary

- Entropy-based detection reliably flags concentrated traffic attacks  
- Real-time flow monitoring with sFlow-RT confirms detection accuracy  
- Bandwidth control mitigates attack without halting benign traffic  
- Future work includes ML-based detection and differentiation from flash crowds

---

##  References

- [Mininet](http://mininet.org/)  
- [POX Controller](https://github.com/noxrepo/pox)  
- [Scapy](https://scapy.net/)  
- [sFlow-RT](https://sflow-rt.com/)  
- [Iperf](https://iperf.fr/)  

---

📩 Contact: mamdouh.eac@gmail.com
