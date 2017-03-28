# chimera
![test](/images/chimera.gif)
![test](/images/plot.png)

Classical simulation of quantum annealing as proposed by this paper: http://arxiv.org/abs/1401.7087 .  Run

    python model.py
    
Some dependencies may be necessary.

# Description
The system is a lattice of 16 clusters, each with 8 qubits (modeled as XZ spins).  Pairwise coupling exists between certain qubits, as per the structure described in the paper.  A specific instance of the problem is determined by whether each coupling is ferromagnetic or antiferromagnetic (that is, whether coupled spins want to be aligned or anti-aligned).

Two magnetic fields are controlled separately, following some annealing schedule.  The first (the A field, pointing along the x-axis) is initially on and forces the spins to start in one pre-defined direction.  This field drops off exponentially.  The second (the B field, pointing along the z-axis) is initially off but slowly turns on, activating the coupling between spins.  The spins are updated via a Metropolis-style rule (where smaller energies are preferred).

The above animation and graph shows a single problem from beginning to end, and the graph of the energy.
