from collections import OrderedDict

import glsl_spec

version_commands = {}
commands_version = {}
version_commands_flat = {}
commands_version_flat = {}

# Maps glColor2d to glColor
function_aliases = {}
# Maps glColor to glColor2d
aliased_functions = {}

example_functions = {}
tutorial_functions = {}

examples = {}

tutorials = {}

def get_major_versions(all_versions):
  major_versions = []
  for v in all_versions:
    major_version = v[:3]
    if not major_version in major_versions:
      major_versions.append(major_version)
      
  return major_versions

def get_major_versions_available(command):
  global commands_version_flat

  versions_available = commands_version_flat[command]
  versions_available.sort()
    
  return get_major_versions(versions_available)

def reverse_version_index(command_list):
  reversed = {}
  
  for version in command_list:
    for command in command_list[version]:
      if not command in reversed:
        reversed[command] = []

      reversed[command].append(version)
      reversed[command].sort()

  return reversed

def generate_versions():
  print "Generating version index..."
  global version_commands
  global commands_version
  global version_commands_flat
  global commands_version_flat
  global function_aliases
  global aliased_functions
  
  version_commands = glsl_spec.version_commands

  for version in version_commands:
    version_commands_flat[version] = []
    
    for command in version_commands[version]:
      if int(version[2]) >= 3:
        if not command in function_aliases:
          function_aliases[command] = version_commands[version][command]

        if not version_commands[version][command] in aliased_functions:
          aliased_functions[version_commands[version][command]] = []
          
        if not command in aliased_functions[version_commands[version][command]]:
          aliased_functions[version_commands[version][command]].append(command)

        if not command in version_commands_flat[version]:
          version_commands_flat[version].append(version_commands[version][command])
          
  commands_version = reverse_version_index(version_commands)
  commands_version_flat = reverse_version_index(version_commands_flat)
  
  for example in examples:
    fp = open('html/examples/' + example + ".htm")
    examples[example]['code'] = fp.read()
    fp.close()
    
    for command in examples[example]['commands']:
      aliased_command = ""
      if command in function_aliases:
        aliased_command = function_aliases[command]
        
      assert aliased_command in commands_version_flat or command in commands_version_flat # This command was typed in wrong.

      if not command in example_functions:
        example_functions[command] = []
      example_functions_entry = {'example': example}
      if 'versions' in examples[example]:
        example_functions_entry['versions'] = examples[example]['versions']
      else:
        example_functions_entry['versions'] = get_major_versions(version_commands.keys())
      example_functions[command].append(example_functions_entry)

      if aliased_command != "" and aliased_command != command:
        if not aliased_command in example_functions:
          example_functions[aliased_command] = []
        example_functions_entry = {'example': example}
        if 'versions' in examples[example]:
          example_functions_entry['versions'] = examples[example]['versions']
        else:
          example_functions_entry['versions'] = get_major_versions(version_commands.keys())
        example_functions[aliased_command].append(example_functions_entry)

  for tutorial in tutorials:
    for command in tutorials[tutorial]['commands']:
      aliased_command = ""
      if command in function_aliases:
        aliased_command = function_aliases[command]

      assert aliased_command in commands_version_flat or command in commands_version_flat # This command was typed in wrong.

      if not command in tutorial_functions:
        tutorial_functions[command] = []
      tutorial_functions_entry = {'tutorial': tutorial}
      if 'versions' in tutorials[tutorial]:
        tutorial_functions_entry['versions'] = tutorials[tutorial]['versions']
      else:
        tutorial_functions_entry['versions'] = get_major_versions(version_commands.keys())
      tutorial_functions[command].append(tutorial_functions_entry)
        
      if aliased_command != "" and aliased_command != command:
        if not aliased_command in tutorial_functions:
          tutorial_functions[aliased_command] = []
        tutorial_functions_entry = {'tutorial': tutorial}
        if 'versions' in tutorials[tutorial]:
          tutorial_functions_entry['versions'] = tutorials[tutorial]['versions']
        else:
          tutorial_functions_entry['versions'] = get_major_versions(version_commands.keys())
        tutorial_functions[aliased_command].append(tutorial_functions_entry)

  print "Done."

command_categories = OrderedDict([
  ( "Trigonometry", [
    "radians", "degrees", "sin", "cos", "tan", "asin",
    "acos", "atan", "sinh", "cosh", "tanh","asinh", "acosh", "atanh"
  ] ),
  ( "Exponential", [
    "pow", "exp", "log", "exp2", "log2", "sqrt", "inversesqrt"
  ] ),
  ( "Common", [
    "abs", "sign", "floor", "trunc", "round", "roundEven", "ceil", "floor", "fract", "mod", "modf", "min", "max", "clamp", "mix", "step", "smoothstep", "isnan", "isinf", "floatBitsToInt",  "intBitsToFloat", "fma", "frexp", "ldexp"
  ] ),  
  ( "Floating-Point Packing", [
    "packDouble2x32","packHalf2x16","packUnorm","unpackDouble2x32","unpackHalf2x16","unpackUnorm"
  ] ),  
  ( "Built-In Variables", [
    "gl_ClipDistance", "gl_CullDistance", "gl_FragCoord", "gl_FragDepth", "gl_FrontFacing", "gl_GlobalInvocationID", "gl_HelperInvocation", "gl_InstanceID", "gl_InvocationID", "gl_Layer", "gl_LocalInvocationID", "gl_LocalInvocationIndex", "gl_NumSamples", "gl_NumWorkGroups", "gl_PatchVerticesIn", "gl_PointCoord", "gl_PointSize", "gl_Position", "gl_PrimitiveID", "gl_PrimitiveIDIn", "gl_SampleID", "gl_SampleMask", "gl_SampleMaskIn", "gl_SamplePosition", "gl_TessCoord", "gl_TessLevelInner", "gl_TessLevelOuter", "gl_VertexID", "gl_ViewportIndex", "gl_WorkGroupID", "gl_WorkGroupSize"
  ] ),
  ( "Geometric", [
    "length", "distance", "dot", "cross", "normalize", "faceforward", "reflect", "refract"
  ] ),  
  ( "Image", [
    'imageAtomicAdd', 'imageAtomicAnd', 'imageAtomicCompSwap', 'imageAtomicExchange', 'imageAtomicMax', 'imageAtomicMin', 'imageAtomicOr', 'imageAtomicXor', 'imageLoad', 'imageSamples', 'imageSize', 'imageStore'
  ] ),  
  ( "Geometry Shader", [
    'EmitStreamVertex', 'EmitVertex', 'EndPrimitive', 'EndStreamPrimitive'
  ] ),  
  ( "Atomic", [
    'atomicAdd', 'atomicAnd', 'atomicCompSwap', 'atomicCounter', 'atomicCounterDecrement', 'atomicCounterIncrement', 'atomicExchange', 'atomicMax', 'atomicMin', 'atomicOr', 'atomicXor'
  ] ),  
  ( "Vector", [
    'all', 'any', 'equal', 'lessThan', 'lessThanEqual', 'greaterThan', 'greaterThanEqual', 'not', 'notEqual'
  ] ), 
  ( "Integer", [
    'umulExtended', 'bitfieldExtract', 'bitfieldInsert', 'bitfieldReverse', 'bitCount', 'findLSB', 'findMSB'
  ] ),
  ( "Texture Sampling", [
    'texture', 'textureGather', 'textureGatherOffset', 'textureGatherOffsets', 'textureGrad', 'textureGradOffset', 'textureLod', 'textureLodOffset', 'textureOffset', 'textureProj', 'textureProjGrad', 'textureProjGradOffset', 'textureProjLod', 'textureProjLodOffset', 'textureProjOffset', 'textureQueryLevels', 'textureQueryLod', 'textureSamples', 'textureSize'
  ] ),
  ( "Memory Barrier", [
    'barrier', 'memoryBarrier', 'memoryBarrierAtomicCounter', 'memoryBarrierBuffer', 'memoryBarrierImage', 'groupMemoryBarrier'
  ] ),
  ( "Matrix", [
    'determinant', 'inverse', 'outerProduct', 'transpose', 'matrixCompMult'
  ] ),    
])

# Functions left to categorize

#dFdx
#floatBitsToint
#fwidth
#interpolateAtCentroid
#interpolateAtOffset
#interpolateAtSample
#outerProduct
#texelFetch
#texelFetchOffset
#uaddCarry
#usubBorrow

generate_versions()
