# Relevance to UOS v2: SEU

## Source-supported comparison

- SEU DDS includes an internal IR+OR `Combination` bearing class. [SEU-E05]
- Its bearing and gear `mixture` is a pooled nine-class classification set, not a simultaneous bearing–gear compound condition. [SEU-E06]
- Two operating controller conditions are reported, but RPM/load conversion, sensor layout, sampling rate, duration, DAQ, and mounting are Unknown. [SEU-E04, SEU-E09]
- Physical label validation is not reported; the evidence is downstream classification performance. [SEU-E07]

## Interpretation for UOS design

SEU adds another precedent against claiming IR+OR as new. It does not materially inform UOS sensor placement, sampling rate, or record length because acquisition details are missing. It also demonstrates why `mixture`, `multi-class`, and `compound fault` must not be treated as synonyms.

## Candidate differentiation to test, not claim

- complete pairwise-plus-triple internal matrix rather than one IR+OR combination;
- actual same-sample bearing–gear or bearing–rotor compounds distinguished from pooled classes;
- explicit synchronized four-channel acquisition and raw timing metadata;
- physically derived sampling/duration and systematic label validation.

## Remaining evidence needed

- official UCI/SEU repository documentation, persistent endpoint, manifest, and license;
- sensor/DAQ/mounting/channel description and raw sampling information;
- exact bearing and gearbox models, defect-generation procedure and severity;
- meaning of the two controller settings in RPM and physical load;
- raw-versus-preprocessed file schema.
