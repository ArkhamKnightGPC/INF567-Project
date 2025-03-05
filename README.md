# Physical Layer Security for Visible Light Communication Systems

Project developed for the course INF567: Wireless Networks at Ecole polytechnique. The goal of this project is to explore different **beamforming techniques** proposed in scientific papers for Physical Layer Security(PLS) to prevent eavesdropping on VLC systems and attempt to replicate their results on an **Octave simulation environment**.

**Table of contents**
- [Introduction](#introduction)
- [Modelisation: Indoor VLC system](#modelisation-indoor-vlc-wiretap-system)
- [Beamforming](#beamforming)
- [References](#references)

## Introduction

The literature review performed on [[1]](#1) was the basis for the bibliography study performed on this project. It is important to highlight that VLC systems are not intended to replace RF technologies. VLC systems are more efficient in indoor environments and are complementary to RF technologies.

We consider an IM/DD MIMO VLC system with multiple *Access Points(APs)*, multiple *Authorized Users(AUs)* and multiple *Eavesdropping devices*.

- **IM** (intensity modulation) refers to the method of encoding information by varying the intensity of the light source, which is then detected by a receiver.

- **DD** (direct detection) refers to the detection of the transmitted signal by directly measuring the intensity of the received light, typically using a photodiode, without needing to decode phase or frequency information.

## Modelisation: Indoor VLC wiretap system

As in [[1]](#1), we consider a room os size $L \times W \times H$. The room is equipped with $M$ APs that are located at its ceiling. The APs act as single transmitters, sending simultaneously $N$ sets of confidential messages to $N$ AUs in the presence of $K$ EDs.

For all $i \in \{1,..,N\}$, the $i$th AU is equipped with $N_i \in \mathbb{N}$ photodiodes and For all $j \in \{1,..,K\}$, the $j$th ED is equipped with $K_j \in \mathbb{N}$ photodiodes.

![modelisation](modelisation.PNG)

## Beamforming

...

## References

<a id="1">[1]</a> Mohamed Amine Arfaoui, Mohammad Dehghani Soltani, Iman Tavakkolnia, Ali Ghrayeb, Majid Safari, Chadi M. Assi, Harald Haas (2020).
**Physical Layer Security for Visible Light
Communication Systems: A Survey** IEEE Communications Surveys and Tutorials.

<a id="2">[2]</a> Simona Riurean (2021).
**A study on the VLC security at the physical layer
for two indoor scenarios** MATEC Web of Conferences.

<a id="3">[3]</a>
Sunghwan Cho, Gaojie Chen, Justin P. Coon (2018).
**Securing Visible Light Communication Systems by Beamforming in the Presence of Randomly Distributed Eavesdroppers** IEEE Transactions on Wireless Communications.
