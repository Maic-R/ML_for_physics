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
Jets are selected which contain a reconstructed secondary vertex, which is a subset of the particles making up the jet which intersect at a common point away from the primary collision point. 
This is a typical signature of a heavy quark jet, but may also arise in light jets due to a mis-reconstruction of the constituent particle trajectories. The goal is to build a machine learning algorithm to classify b-jets, c-jets and light jets.

## Dataset description

Dataset contains jet data simulated considering pp interactions at the LHCb experiment. When there is a jet, what one does is look among the constituent track of the jet, to see if there are pairs/triplets (or combinations with a variable number) pf tracks that can be associated to a decay vertex. Afterward, it is possible to select the jet depending on the properties of the secondary vertex. Most of the times there are multiple secondary vertices per jet, but with selection criteria it is possible to discard most of them. If more than one secondary vertex associated to a jet remains, the situation can be handled in several ways.

The dataset contains three csv files: 

- **ljet_training.csv**: label `mc_flavour = 0` for light jets
- **cjet_training.csv**: label `mc_flavour = 4` for c-jets
- **bjet_training.csv**: label `mc_flavour = 5` for b-jets

and another file (**competitionData.csv**) to test the model (no label are provided in this file).

The header of these csv files is constituted by 15 different variables, representing information on both jet and secondary vertex associated to the jet.

### Dataset features

This is a possible interpretation of the variables in the csv headers, that represent the feature of the datasets:

- **PT:** transverse momentum of the jet

- **ETA:** pseudorapidity of the jet

- **mc_flavour:** the "true" particle that generated the jet in the simulation. It is basically the label of each class

- **drSvrJet:** difference of R between the secondary vertex and the jet, $\Delta R = \sqrt{\Delta \phi^2 + \Delta \eta^2}$. $\Delta R$ represents the angular separation between two objects. Therefore small $\Delta R$ indicates that the two objects are close in angle and may be correlated. Large values of $\Delta R$ indicates instead that the two objects are unlikely to be physically correlated.
<span style="color:green;">
This variable could be usefull to distinguish jets with secondary vertices (heavy flavour jets) from those without secondary vertices
</span>

- **fdChi2:** can be something related to the quality of the secondary vertex or the $\chi^2$ of the flight distance (that measures the distance between primary and secondary vertices)

- **fdrMin:** could be the minimum flight distance significance (flight distance divided by its uncertainaty), that measures how separated secondary vertex is from primary one

- **m:** mass of the secondary vertex

- **mCor:** corrected mass of the secondary vertex. It is defined as: $m_{corr}(DV) = \sqrt{m(DV)^2 + [p(DV)sin\theta]^2} + p(DV)sin\theta$, where $\theta$ is the angle between the DV momentum and its direction of flight.

- **mCorErr:** error on corrected mass

- **nTrk:** the number of tracks associated to the secondary vertex. A higher number of tracks indicates a more complex decay topology

- **nTrkJet:** number of tracks in the entire jet. It should be less than nTrk, but taking a look at c-jets dataset what I see is that nTrk $\ge$ nTrkJet. So this has to be understood better 

- **pt:** transverse momentum of a constituent particle or track

- **ptSvrJet:** transverse momentum of the secondary vertex relative to the jet. It measures the momemntum fraction carried by the secondary vertex tracks

- **tau:** lifetime of the decaying particle that formed the secondary vertex.
<span style="color:green;">
For high-flavour jets we should expect higher lifetimes compared to light flavour ones
</span>

- **ipChi2Sum:** sum of $\chi^2$ values of the impact parameters of tracks in the secondary vertex. Quantifies the consistency of the tracks displacement from the primary vertex. $\chi^2_{IP}$ is defined as the difference in the vertex-fit $\chi^2$ of the PV reconstructed with and without the track under consideration


Comment on PT and pt: PT is an aggregate property of the entire jet, while pt breaks it down into individual components, namely the transverse momentum of specific particles or tracks in the jet. By examining pt it is possible to study the distribution of momentum within the jet. In jet tagging applications heavy flavour jets often have high-momentum tracks from decay products, which might stand out in the pt spectrum compared to light-flavour jets.

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