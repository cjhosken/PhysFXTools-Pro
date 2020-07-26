PhysFX
===============

PhysFX is a Blender tool used to help users speed up their workflow in physics simulations.

Usage
-----
* Install Blender 2.81 or greater: https://www.blender.org/download/
* Under File > User Preferences... > Add-ons > Install From File... open the downloaded ZIP file
* Under File > User Preferences... > Add-ons enable this script (search for "PhysFX")
* Locate the toolbar in the 3D View under Properties > PhysFX

How it works
------------

GLUE TOOL:
* Locates all the objects in the parent collection.
* Compares each object with one another to see if they have any intesecting (or close) faces.
* Creates empties between objects that have intecting (or close) faces.
* Makes the empty a rigid body constraint.
* Moves all the created empties into a new collection (named after the parent collection).


PROXYMESH TOOL:
* Creates a cube with the same dimensions as the object.
* Subdivides the cube 6 times.
* Shrinkwraps the cube to the surface of the object.
* Remeshes the cube.
* Parents the cube to the object.


GROUP COLLISIONS TOOL:
* Locates all the selected objects.
* adds the collision modifier.


Credits
------
Released under the [GPL License].

Authored and maintained by Christopher Hosken.

> Email [blendervcg@gmail.com] 
> Instagram [@visual_cg](https://www.instagram.com/visual_cg/)
> Artstation [Christopher Hosken](https://www.artstation.com/visualcg)

[GPL License]: http://www.gnu.org/licenses/gpl-3.0.html
