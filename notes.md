# Jet tagging with LHCb simulated data

## Introduction
In proton-proton collisions a lot of high energy quarks and gluons are produced. Due to color confinement quarks and gluons hadronise, producing a narrow stream of high energy particles, known as jet.
One important aspect is the identification of jet flavour, namely understand which quark (or gluon) generated the jet. This is know as jet tagging.

Typically the flavour of a jet can be of two types:

- **heavy flavour**: are jets that aries from the hadronisation of a bottom or charm quark

- **light flavour**: are jets generated from the hadronisation of light quarks as well as gluons

\
<span style="color:green;">
Heavy flavour jets are distinguished from light jets by the long lifetime of the quarks involved, typically resulting in a subset of particles within the jet displaced from the primary collision point.
</span>

\
The dataset contains data simulated at the LHCb experiment.
**Jets are selected using events that contain a reconstructed secondary vertex**, which is a subset of the particles making up the jet which intersect at a common point away from the primary collision point. 
This is a typical signature of a heavy quark jet, but may also arise in light jets due to a mis-reconstruction of the constituent particle trajectories. The goal is to build a machine learning algorithm to classify b-jets, c-jets and light jets.

## Dataset description

Dataset contains jet data simulated considering pp interactions at the LHCb experiment. When there is a jet, what one does is look among the constituent track of the jet, to see if there are pairs/triplets (or combinations with a variable number) of tracks that can be associated to a decay vertex. Afterward, it is possible to select the jet depending on the properties of the secondary vertex. Most of the times there are multiple secondary vertices per jet, but with selection criteria it is possible to discard most of them. If more than one secondary vertex associated to a jet remains, the situation can be handled in several ways.

The dataset contains three csv files: 

- **ljet_training.csv**: label `mc_flavour = 0` for light jets
- **cjet_training.csv**: label `mc_flavour = 4` for c-jets
- **bjet_training.csv**: label `mc_flavour = 5` for b-jets

and another file (**competitionData.csv**) to test the model (no label are provided in this file).

The header of these csv files is constituted by 15 different variables, representing information on both jet and secondary vertex found in the jet cone.

### Dataset features

Note: we can think that a jet is a particle, as well as the secondary vertex. So we can refer to transverse momentum of the jet or SV, as well as the pseudorapidity and other quantities.

- **PT:** transverse momentum of the jet. $p_T = \sqrt{p_x^2 + p_y^2}$, component of the total momentum perpendiculare to the beam axis (z-axis)

- **ETA:** pseudorapidity of the jet. $\eta = -ln(tan(\frac{\theta}{2}))$, related to polar angle (angle respect to the beam axis)

- **mc_flavour:** the "true" particle that generated the jet in the simulation. It is basically the label of each class

- **drSvrJet:** difference of R between the secondary vertex and the jet, $\Delta R = \sqrt{\Delta \phi^2 + \Delta \eta^2}$. Usually the SV will be displaced from the jet axis; $\Delta R$ represents the angular separation between two objects. Therefore small $\Delta R$ indicates that the two objects are close in angle and may be correlated. Large values of $\Delta R$ indicates instead that the two objects are unlikely to be physically correlated.
<span style="color:green;">
This variable could be usefull to distinguish jets with secondary vertices (heavy flavour jets) from those without secondary vertices.
</span>
In this dataset however, all the three type of jets contains a secondary vertex, so it might not be that useful to discriminate between light and heavy flavour jets

- **fdChi2:** $\chi^2$ of the flight distance, that represents the distance between primary and secondary vertices. It is the distance travelled by the particle before decaying

- **fdrMin:** 

- **m:** invariant mass of the secondary vertex

- **mCor:** corrected mass of the secondary vertex. It is defined as: $m_{corr}(DV) = \sqrt{m(DV)^2 + [p(DV)sin\theta]^2} + p(DV)sin\theta$, where $\theta$ is the angle between the DV momentum and its direction of flight. The corrected mass is the minimum mass that the long-lived hadron can have that is consistent with the direction of flight.
It should be important to discriminate between c and b jets.

- **mCorErr:** error on corrected mass

- **nTrk:** the number of tracks associated to the secondary vertex. A higher number of tracks indicates a more complex decay topology

- **nTrkJet:** number of tracks in the jet cone. Some of the tracks of the SV (`nTrk`) may be outside the jet cone. So this variable should be, most of the times, equals to `nTrk`. 
Based on _Identification of charm and beauty jets_ paper, this variable could represent the number of SV tracks with $\Delta R$ < 0.5 relative to the jet axis

- **pt:** transverse momentum of the SV

- **ptSvrJet:** transverse momentum of the secondary vertex relative to the jet. It measures the momemntum fraction carried by the secondary vertex tracks. \
So it is the ratio $\dfrac{p_T(SV)}{p_T(jet)}$

- **tau:** lifetime of the decaying particle that generated the secondary vertex.
<span style="color:green;">
For high-flavour jets we should expect higher lifetimes compared to light flavour ones
</span>

- **ipChi2Sum:** sum of $\chi^2$ values of the impact parameters of tracks in the secondary vertex. Quantifies the consistency of the tracks displacement from the primary vertex. $\chi^2_{IP}$ is defined as the difference in the vertex-fit $\chi^2$ of the PV reconstructed with and without the track under consideration


Comment on PT and pt: PT is an aggregate property of the entire jet, while pt breaks it down into individual components, namely the transverse momentum of specific particles or tracks in the jet. By examining pt it is possible to study the distribution of momentum within the jet (the ones that are associated to the SV). \
<span style="color:green;">
In jet tagging applications heavy flavour jets often have high-momentum tracks from decay products, which might stand out in the pt spectrum compared to light-flavour jets.
</span>

## Notes from "Identification of charm jets at LHCb" paper

Charm jets are defined as those that have a promptly produced and a weakly decadying c hadron with transverse momentum pT > 5 GeV within the jet cone. Therefore, the tagging of c jets is performed using displaced vertices (DVs) formed from the decays of such c hadrons.

DV candidates are reconstructed using good-quality tracks both within and outside of the jet, with pT > 0.5 GeV and $\chi^2_{IP}$ > 9, where $\chi^2_{IP}$ is defined as the difference in the vertex-fit $\chi^2$ of the PV reconstructed with and without the track under consideration. Tracks are combined into two- and three-body DVs, which are required to form a good-quality vertex, be downstream of the PV, and have an invariant mass greater than 0.4 GeV and less than that of the B<sup>0</sup> meson.

Two- and three-body DV candidates that pass these requirements and share one or more tracks are linked together to form n-body DVs. All DVs candidates are subsequently required to have $p_T$ > 2 GeV and a significant separation from all PVs.

A DV that probably originated from the decay of a c-hadron, will have two, three or four tracks associated. More than 4 tracks $\rightarrow$ b-hadron.

**Requirements on DVs reconstruction:**

- good-quality tracks within and outside the jet, with $p_T$ > 0.5 GeV and $\chi^2_{IP}$ > 9
- $m_{corr}$ > 0.6 GeV
- uncertainaty on $m_{corr}$ < 0.5 GeV
- $\Delta R$ < 0.5

## Notes from "Identification of charm and beauty jets" paper
Events recorded due to the presence of a (b, c)-hadron decay require that at least one track should have $p_T$ > 1.7 GeV and $\chi^2_{IP}$ with respect to any primary interaction greater than 16, where $\chi^2_{IP}$ is defined as the difference in $\chi^2$ of a given primary pp interaction vertex (PV) reconstructed with and without the considered track.

<span style="color:green;">
Decays of b hadrons are inclusively identified by requiring a two-, three- or four-track secondary vertex (SV) with a large sum of $p_T$ of the
tracks and a significant displacement from the PV.
</span>

A specialized boosted decision tree (BDT) algorithm is used for the identification of SVs consistent with the decay of a b hadron.