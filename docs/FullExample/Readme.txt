After running the following line:
python BuildContainersGraph.py -a build -t ContainerStaticTopology-11Services.csv -c CveList-11Services.csv -m containerModelAndVul.p

It creates containerModelAndVul.p (which is also attached).

You should copy containerModelAndVul.p and Container_IRs.p to MulVAL's environment, let's say, to the testcases folder.
Then run from the utils folder:
graph_gen.sh -r ../testcases/Container_IRs.p -v -p ../testcases/containerModelAndVul.p

utils/AttackGraph.pdf is the generated AG

You can add --simple before -p to get an attack graph with numbers, and their description will be in AttackGraph.txt

The result for these topology and CVEs is AttackGraph-11Services.pdf and AttackGraph-11Services.txt (which is the AG presented in the paper).