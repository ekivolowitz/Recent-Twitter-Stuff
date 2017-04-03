# Recent-Twitter-Stuff

<h2>Dependencies for the machine executing the script:</h2>
<ol>
<li>MongoDB Daemon (must always be running in the background)</li>
<li>Mongo Client (not technically necessary but this allows you to interface with mongodb outside of python to verify work)</li>
<li>tweepy (for python 3.X)</li>
<li>pymongo (for python 3.X)</li>
</ol>

Twitter research for constructing social networks for audience segmentation.

<h2>USAGE: python3 GetData.py \<twitter ID or handle></h2>

<h2> I would strongly recommend running this script as a headless command on a remote machine. In order to do this, you must run
 
ssh username@remote-machine-address "python3 path/to/script/GetData.py <username>"</h2>
