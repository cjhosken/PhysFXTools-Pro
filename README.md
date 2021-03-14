# PhysFX Tools Pro

PhysFX Tools is a Blender addon used to help users speed up their workflow in physics simulations.

## Installation
* Install Blender 2.9 or greater: https://www.blender.org/download/
* Under File > User Preferences... > Add-ons > Install From File... open the downloaded .zip file
* Under File > User Preferences... > Add-ons enable this script (search for "PhysFXTools-Pro")
* Locate the toolbar in the 3D View under Properties > PhysFX-Tools

## Usage

### Glue
To use Glue tool...

1. Either select a group of objects, or a collection.
2. Enable the 'Use Collection' box if you are selecting a collection.
3. Specifiy a glue strength (-1 is indestructable)
4. Specificy a glue distance. If the distance between two objects is greater than this, they will not be glued.
5. Press the 'Glue' button.

If you wish to delete the glue, either select the parent collection or the glue collection. Glue removal iterates through child collections, so if you have the 'Scene Collection' selected all glue will be removed. Once you have you collection selected, press the 'x' button.


### Proxy Mesh
To use the Proxy Mesh tool...
1. Select 1 or more objects.
2. Specify a resolution and offset.
3. Press the 'Create Proxy' button.

If you wish to remove the proxy mesh, simply select and delete it. The 'x' button is use to remove ALL proxy meshes in the scene.


### Grouping
The grouping tool has 2 subpanels. One for the collision modifier and one for rigid bodies. To use each...
1. Select 1 or more objects.
2. Input what settings you need.
3. Press the 'Group Collisions' button.

If you wish to remove the effects, select the object and then press the 'x' next to the button.


### Soft Body Presets
The Soft Body Presets panel is used to help speed up the process of creating soft bodies. To add a softbody to an object...
1. Select an object.
2. Click the 'Add Softbody' button.

if you wish to remove the softbody...
1. Select an object.
2. Press the 'x' button.

If an object has a softbody modifier, the 'Presets:' label will brighten. If you press the menu icon next to the 'Presets:' label, you will be able to use the built in PhysFX softbody presets.

### Cell Fracture
The Cell Fracture panel will only be accessable if you have the Cell Fracture addon enabled. Usage is fairly simple.
1. Select an object.
2. Click the 'Cell Fracture' button.
3. Edit the settings.

The '+' button will import the PhysFX presets into your blender version.

### Extra
The Extra panel is where you can report a bug or get in contact with me, the author.

# Credits
Released under the [GPL License].

Authored and maintained by [Christopher Hosken](https://github.com/Christopher-Hosken).

Email [hoskenchristopher@gmail.com] 

Instagram [@cjhosken](https://www.instagram.com/cjhosken/)

Artstation [Christopher Hosken](https://www.artstation.com/christopherhosken)

Discord [@Cjhosken#7147]

## License
[GPL License](http://www.gnu.org/licenses/gpl-3.0.html)