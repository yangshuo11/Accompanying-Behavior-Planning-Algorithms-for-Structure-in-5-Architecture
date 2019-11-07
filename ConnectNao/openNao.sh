cd

gnome-terminal --window --tab -e 'bash -c "~/OwnApp/NaoEnvironment/Nao_connector/bin/naoqi-bin -p 10086;exit;exec bash;"' --tab -e 'bash -c "~/OwnApp/NaoEnvironment/Nao_connector/choregraphe;exit;exec bash;"' --tab -e 'bash -c "roscore;exit;exec bash;"' --tab -e 'bash -c "cd;cd ~/OwnApp/V-REP;./vrep.sh;exit;exec bash;"'

#cd 
#cd OwnApp/VREP_3_4_0
#./vrep.sh
#gnome-terminal -x bash -c  "./OwnApp/Nao_connector/bin/naoqi-bin -p 10086;exit;exec bash;"

#gnome-terminal


 

