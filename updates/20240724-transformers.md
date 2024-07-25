# Transformers (WIP)

Okay, so: it's pretty easy to get [an RF transformer](https://eu.mouser.com/ProductDetail/994-SWB1040-PCL), but they're typically only rated for 0.25W.

However, even though our pulse power is 4.5W, our duty cycle may only be something like 5%, putting our average power at 0.225W (which is below the 0.25W rating).

We need to **stress test in real-life**, but the theoretical constraints are:

- Overheating: should be fine, since that depends more on average power than peak power
- Core saturation: ferrite should be able to go kinda high, so should be fine, but let's test it