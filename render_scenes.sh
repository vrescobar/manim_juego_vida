#!/bin/bash

scenes=(SceneRandom SceneGlider SceneIntro SceneRules ScenePostRules SceneRPentomino SceneStillLife SceneOscillators SceneGliderGun SceneCopperhead SceneQuestion)
counter=1

for scene in "${scenes[@]}"; do
  padded_counter=$(printf "%02d" $counter)
  manimgl app.py $scene --hd -w --file_name "AppLife_${padded_counter}_$scene.mp4"
  counter=$((counter + 1))
done