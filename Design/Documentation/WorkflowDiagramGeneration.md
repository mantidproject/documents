#Workflow Diagram Generation

## Motivation

Currently, only a subset of the workflow algorithms in Mantid have flow charts
documenting their behaviour. These flow charts have been created with different
tools, in different styles. This inconsistency can easily cause confusion.

In addition, the diagrams themselves are stored and `.png` files within the git
repository. This is not particularly efficient when they're updated as git
stores a complete copy of each version.

## Proposed Approach

In future, the flow diagrams should be created in the `.dot` format, a plain 
text file format that defines a graph declaratively and some options for how
the edges and vertices should be drawn. This approach has already been used
for a few of the diagrams:

* https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Framework/WorkflowAlgorithms/doc/diagrams/ReflectometryReductionOne.dot
* https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Framework/WorkflowAlgorithms/doc/diagrams/ReflectometryReductionOneAuto-Groups.dot
* https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Framework/WorkflowAlgorithms/doc/diagrams/ReflectometryReductionOneAuto-PolarizationCorrection.dot
* https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Framework/WorkflowAlgorithms/doc/diagrams/AlignAndFocusPowderFlowchart.dot

These simple `.dot` file are easy to diff and update, which is perfect for git.
For display, these files can be processed as part of the build, by a tool
called `graphviz` to create `.png` images. `graphviz` is already optionally
used by Doxygen to draw its dependency graphs.

This approach also provides an easy way to tackle the inconsistencies between
the various diagrams. The styling instructions in each diagram can be templated,
and filled in with the correct instructions by a Python script.

My suggested approach to performing this pre-processing step on the dot files is
using `string.Template` in python (available in 2.4+). As this script could be
executed using Mantid, like `build_sphinx`, and requires no additional
dependencies other than graphviz itself.

The script itself could be very simple. This is a rough example:

```python
from string import Template

style = dict()

style["global_style"] = """
fontname = Helvetica
labelloc = t
node[fontname="Helvetica", style = filled]
edge[fontname="Helvetica"]
"""
style['param_style']     = 'node[fillcolor = khaki, shape = oval]'
style['decision_style']  = 'node[fillcolor = limegreen, shape = diamond]'
style['algorithm_style'] = 'node[style = "rounded,filled", fillcolor = lightskyblue, shape = rectangle]'
style['process_style']   = 'node[fillcolor = lightseagreen, shape = rectangle]'
style['value_style']     = 'node[fontname = "Times-Roman", fillcolor = grey, shape = parallelogram]'

#Pseudocode follows
#for each diagram.dot
#   dot_src = Template(file_contents)
#   dot_src.substitute(style)
#   run `dot -o diagram.png` and pipe dot_src into stdin
```

...and then the dot files would look like this:

```dot
digraph ReflectometryReductionOne {
  label = "ReflectometryReductionOne Flowchart"
  $global_style

  subgraph params {
    $param_style
    inputWorkspace    [label="InputWorkspace"]
    ...
  }

  subgraph decisions {
    $decision_style
    checkXUnit      [label="X axis in &lambda;?"]
    ...
  }

  subgraph algorithms {
    $algorithm_style
    calcTheta       [label="SpecularReflectionCalculateTheta"]
    ...
  }

  subgraph processes {
    $process_style
    directBeamNorm  [label="Perform Direct\nBeam Normalisation"]
    ...
  }

  subgraph values {
    $value_style
    valMon          [label="I&#8320;(&lambda;)"]
    ...
  }

  inputWorkspace    -> checkXUnit
  checkXUnit        -> checkThetaIn     [label="Yes"]
  checkXUnit        -> convertToWL      [label="No"]
  ...
}
```

This approach means the existing dot files can be used almost verbatim,
the styling options are simply substituted in.

### Pros
* Diagrams are kept visually consistent
* Diagrams are easy to update
* Fewer binary files in the repository
* Changes to styling propagate across all diagrams automatically

### Cons
* `graphviz` required to build documentation
* Additional complexity in the build process
* We get to bikeshed over the styling conventions
