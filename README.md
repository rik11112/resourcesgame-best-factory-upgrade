# Optimal Factory Upgrade Calculator

With all the great websites and tools out there, I was wondering if there was an easy way to see which factory upgrade earns itself back the quickest, and therefore is the best bang for your buck. I found a very helpful website r.jakumo.org which calculates the earnback time, but it lacked the option to easily compare factories. So I wrote a script to compare the factories based on the earnback time from r.jakumo.org. (I hope that's allowed, if not let me know)

## Example Script Result:

```
name                days toLvl price 
Oil refinery        4.7  4     1.9B  
Concrete factory    6    16    1.4B  
Fertilizer factory  6.1  3     321.7M
Ironworks           6.7  4     904.3M
Brick factory       6.8  24    324.0M
Glazier's shop      7    4     2.4B  
Copper refinery     7    4     3.7B  
Insecticide factory 7.5  2     1.1B  
Lithium refinery    7.9  2     2.8B  
Silicon refinery    8.9  1     450.1M
Aluminium factory   9.2  4     5.7B  
Plastic factory     10.7 3     2.0B  
Arms factory        12.5 2     9.7B  
Battery factory     17.1 2     5.8B  
```

This is an example of what the script outputs.

## How to use:

1. Install python, and then the required libraries (run these in command prompt):

```bash
pip install requests
pip install beautifulsoup4
```

2. Copy the code into a .py file (at the bottom of the post) and input your info:

![links exampkle](https://github.com/rik11112/resourcesgame-best-factory-upgrade/assets/76134097/dbf71324-a51a-4906-957b-8e49534f4111)

^put in True if you have access to the factory here

![levels example](https://github.com/rik11112/resourcesgame-best-factory-upgrade/assets/76134097/fd8cf3e3-92de-459d-9f1b-c48a2d012619)

^edit the lvl to match your account here

3. Finally, run the script:

```bash
python your_script_file_name.py
```
