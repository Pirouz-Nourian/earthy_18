### Structural Analysis & Optimization
The domes would of earthbags and bottles. Retaining wall and columns would be made of adobe bricks and the textile roof would be made of recycled tent fabric. Form-finding is performed in Kangaroo with the inputs of particles, springs, forces and anchor points, which are retrieved from a given lay-out. 
<br /> <br /> With the initial mesh from Form-Finding procedure and Material properties from the laboratory test and literature, the structural analysis is performed in GH using plugin Karamba, combined with Load and Resistance Factor Design (LRFD) method. The optimization focus on span, height and openings instead of cross section size according to pre-tests. Details can be found in Brick-breaking Report and Structural Analysis Report.

![workflow outline of the design process2](https://user-images.githubusercontent.com/43637877/48030864-ac5acd80-e152-11e8-9e42-e52effce61c5.png)

### Pseudocode
Input Kangaroo mesh<br />
Define the mesh as a shell and Cull unconnected nodes in the model <br />
Input Material properties (density, Young’s modulus, shear modulus, strength)<br />
Define cross section<br />
Define supports points as fixed supports and Cull the duplicate supports<br />
Define loads (live loads and self-weight)<br />
Assemble and Analyze model<br />
Define Time A=0<br />
If the stress and the deformation >= design limit and Time A < 5:<br />
&nbsp; &nbsp; Time A= Time A + 1;<br />
&nbsp; &nbsp; If all the ground levels of domes = 0m or domes are separated:<br />
&nbsp; &nbsp; &nbsp; &nbsp; Change the height of the mesh and Re-analyze model<br />
&nbsp; &nbsp; Else: Separate the domes, Re-define supports points and Re-analyze model<br />
Define Time B =0<br />
If the stress and the deformation >= design limit and Time B < 5:<br />
&nbsp; &nbsp; Time B= Time B + 1;<br />
&nbsp; &nbsp; Change the size of openings and Re-analyze model<br />
Define Time C =0<br />
If the stress and the deformation >= design limit and Time C =0:<br />
&nbsp; &nbsp; Time C= Time C + 1<br />
&nbsp; &nbsp; Add plinth around the domes and Re-analyze model<br />
Read the height, span, stress and deformation of the domes<br />
Output the final mesh

![final mesh](https://user-images.githubusercontent.com/43637877/48030999-0d82a100-e153-11e8-85af-c15ac86f50a6.png)

![table](https://user-images.githubusercontent.com/43637877/48031027-28edac00-e153-11e8-81b9-bc4352200ac7.png)

### Construction
The construction are divided into two stages:
1.	The construction of the tall adobe brick columns and installation of the roof,
*	Marking positions of the anchors.
*	Anchoring the roof fabric underground and laying bricks of columns.
*	Hoisting the fabric up to the columns.
2.	The construction of bottles and earth-bags domes
*	Making bottles or earth-bags elements.
*	Marking positions of the domes.
*	Laying bottles with ropes or earth-bags with barbed wires 

