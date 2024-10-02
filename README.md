# openFUS: a cheap, open-source, easy to replicate FUS device for hackers & researchers

View [current design (subject to change)](/design/) 

### Background

Transcranial focused ultrasound (tFUS) is a non-invasive neuromodulation technique, which has millimeter precision and can reach any depth in the brain. It's safe, and has been used in humans to:

- [improve mood](https://www.frontiersin.org/articles/10.3389/fnhum.2020.00052)
- [reduce sensitivity to pain](https://www.jneurosci.org/content/44/8/e1011232023) (and [again](https://www.sciencedirect.com/science/article/pii/S1935861X20302746))
- [decrease amygdala activity (for treating anxiety)](<https://www.brainstimjrnl.com/article/S1935-861X(24)00040-8/fulltext>)

It's incredible that we have a **non-invasive** way to do the equivalent of putting a wire _anywhere_ in the brain and stimulating it. Why isn't this everywhere?

1. tFUS is relatively new & underdeveloped. It's quickly gaining steam (see [Prophetic](https://x.com/PropheticAI), etc.), but good human studies really only started coming out in the late 2010s!
2. It's still niche in academia, and the hardware is expensive. This means relatively few labs can do it.
3. No good treatment protocols, which makes effect sizes sub-therapeutic. We have the tool but we don't quite know how to use it (sonication parameters, environment, sequence / repetitions, etc.)

### How tFUS works

You wouldn't expect ultrasound could modulate the brain — electric currents or magnetic fields, sure, but acoustic waves? Apparently yes! The mechanisms are still unknown, but by changing the parameters of the ultrasound pulses, you can control whether you get a net excitatory or inhibitory effect.

Then, in order to get the ultrasound to the right part of the brain, you need to focus it. This can be done in many ways, but the easiest to illustrate, is if you have a bunch of weak ultrasound beams, which all converge at the same point:

![how focused ultrasound works](/resources/how_focused_ultrasound_works.jpg)

The beam will be too weak to do anything at the surface, but at the focal point, it will be strong enough to affect neurons.

### Motivation for **openFUS**

Let's compare tFUS to EEG. Nowadays, every neuroscience _undergrad_ is working with EEG (because [OpenBCI](https://openbci.com/) sells $1000 EEGs). Even hackers and psychonauts can use it to make discoveries (for example, [Jhourney](https://x.com/stephen_zerfas/status/1755149844921057744) finding neural correlates of the 2nd jhana).

We've not reached this moment with tFUS yet, but when we do, it's gonna lead to [an explosion in neuroscience](https://sarahconstantin.substack.com/p/testing-human-augmentation) since we can easily and rapidly test hypotheses. Sonicate one area, give a subjective report, take an fMRI, repeat.

For this neuroscience renaissance to happen, **FUS needs to be more accessible**. We need an open-source starting point for engineers to build on top of, and independent researchers to buy and use.

**North star:** make a device theoretically capable of replicating ["Transcranial Focused Ultrasound to the Right Prefrontal Cortex Improves Mood and Alters Functional Connectivity in Humans"](https://www.frontiersin.org/articles/10.3389/fnhum.2020.00052), for less than $1k.

### Contributing

We need your help! Here are some things you can help out with:

- Great software (for neuronavigation, setting sonication params, self-blinding, peer-to-peer science, etc.)
- Great product design (for the handheld device itself)
- Driving electronics (e.g. amplify to generate LOTS of power as cheap as possible)
- Funding (we're not spending any time fundraising, but if you can wire cash with low overhead, it'd help a lot)

If you're interested in contributing, please reach out to Louis Arge [on Twitter](https://x.com/louisvarge), [by email](mailto:louis@muditalabs.ai), or if you have something very concrete: just open a PR.
