# Woops: Soldering is hard

So, turns out AD9833 is *tiny*, which means it's complicated to solder. Didn't realize this.

The [AD9833](https://eu.mouser.com/ProductDetail/Analog-Devices/AD9833BRMZ-REEL7?qs=BpaRKvA4VqGlyZCX2gCZvQ%3D%3D) uses **MSOP-10** which is the very small 10-pin SMD (surface-mount) interface. The [THS3091](https://eu.mouser.com/ProductDetail/Texas-Instruments/THS3091D?qs=ZmJdcv7QZ9r%252B6oHoPq%2FUDQ%3D%3D&countryCode=DE&currencyCode=EUR) uses **SOIC-8**.

For the two types of SMD, we can use **breakout boards** that convert from **[the SMD] to DIP**. You can directly attach jumper wires to DIP.
- [MSOP-10 Breakout Board](https://dk.farnell.com/aries/lcqt-msop10/ic-adaptor-10msop-to-dip-2-54mm/dp/2476034)
- [SOIC-8 Breakout Board](https://dk.farnell.com/aries/lcqt-soic8-8/ic-adaptor-8-soic-to-dip-2-54mm/dp/2476033)

### How to solder (ChatGPT cheatsheet)

Sure, let's get you started with soldering! Here's a beginner's guide to help you solder an MSOP-10 onto an adapter.

### **Concepts**

1. **Soldering**: The process of joining two or more electronic components together by melting solder around the connection. The solder cools and forms a permanent bond.

2. **Solder**: A metal alloy used to create a conductive joint between metal surfaces. Typically, it's a mixture of tin and lead, but lead-free solders are also common.

3. **Flux**: A chemical cleaning agent used to remove oxidation from the metal surfaces to be soldered, allowing the solder to flow and bond more effectively.

### **Ingredients and Tools**

1. **Soldering Iron**: A tool with a heated tip to melt the solder. For your task, a fine tip is recommended.
   - Temperature: Adjustable (350-400°C or 662-752°F).

2. **Solder**: Thin wire solder, preferably 60/40 tin-lead or a lead-free alternative.

3. **Flux Pen or Paste**: Helps the solder flow better and prevents oxidation.

4. **Soldering Iron Stand**: To safely hold the hot soldering iron when not in use.

5. **Sponge or Brass Wire Cleaner**: For cleaning the soldering iron tip.

6. **Tweezers**: To hold small components in place.

7. **Magnifying Glass or Microscope**: To see small components clearly.

8. **Desoldering Braid or Pump**: To remove excess solder if needed.

9. **MSOP-10 Adapter**: The adapter you will solder the MSOP-10 onto.

10. **ESD Mat and Wrist Strap**: To prevent electrostatic discharge from damaging sensitive components.

### **Steps**

1. **Preparation**:
   - Clean the workspace.
   - Secure the MSOP-10 adapter on a non-slip mat or a PCB holder.
   - Put on the ESD wrist strap and ensure it’s grounded.

2. **Tin the Soldering Iron Tip**:
   - Heat the soldering iron.
   - Apply a small amount of solder to the tip once it’s hot.
   - Wipe the tip on the sponge or brass wire cleaner to remove excess solder.

3. **Apply Flux**:
   - Use a flux pen or paste to apply a small amount of flux to the pads of the MSOP-10 adapter.

4. **Position the MSOP-10**:
   - Use tweezers to carefully place the MSOP-10 chip on the adapter, aligning the pins with the pads.

5. **Tack Solder One Pin**:
   - Heat the pad and pin with the soldering iron, then apply a small amount of solder. This will hold the chip in place.

6. **Solder the Remaining Pins**:
   - Apply a small amount of solder to the tip.
   - Touch the soldering iron to each pin and pad briefly, allowing the solder to flow and form a joint.
   - Repeat for all pins, ensuring no solder bridges form between pins.

7. **Inspect the Joints**:
   - Use a magnifying glass or microscope to inspect each solder joint.
   - If there are solder bridges, use the desoldering braid or pump to remove excess solder.

8. **Clean the Board**:
   - Remove any residual flux with a suitable cleaner if necessary.

### **Tips**

- **Patience**: Take your time, especially with small components.
- **Practice**: Practice on some scrap components or old PCBs if possible.
- **Safety**: Work in a well-ventilated area and be cautious with the hot soldering iron.

### **Troubleshooting**

- **Cold Joints**: If the solder joint looks dull or grainy, it’s a cold joint. Reheat the joint and apply a bit more solder.
- **Bridges**: If solder bridges between pins, use desoldering braid or a solder sucker to remove excess solder and retry.

That's the basic rundown! Soldering can be tricky at first, especially with small components, but with practice, you'll get the hang of it. Good luck!