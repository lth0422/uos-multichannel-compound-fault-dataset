# Hardware Inventory and Acquisition Constraints

Last reviewed: 2026-07-16

## Status conventions

- **Confirmed purchase**: 연구팀이 구매 사실과 비용을 제공함
- **Official specification**: 제조사 공식 문서에서 확인함
- **Supplier specification**: 공급사 공개 자료에서 확인했으나 제조사 원본/납품 사양서 재확인 필요
- **Inference**: 확인된 사양으로부터 도출한 설계 해석이며 최종 설정이 아님

## Confirmed purchases

| Category | Product | Quantity | Reported purchase amount | Status |
|---|---|---:|---:|---|
| DAQ module and chassis | NI-9234 + NI cDAQ-9171 | 1 set | KRW 5,086,400 | Confirmed purchase |
| Accelerometer | HS Sensors 13A131 | 4 | KRW 2,860,000 | Confirmed purchase |

The amounts above are user-provided procurement facts. Invoice details, part-number variants, cable accessories, and calibration certificates have not yet been reviewed.

## NI-9234

Verified from the NI-9234 Datasheet:

| Item | Verified specification |
|---|---|
| Analog inputs | 4 channels |
| ADC | 24-bit delta-sigma, analog prefiltering |
| Sampling mode | Simultaneous |
| Maximum internal-timebase rate | 51.2 kS/s per channel |
| Internal-timebase rate rule | `fs = 13.1072 MHz / (256 × n)`, integer `n = 1..31` |
| Example native rates | 51.2, 25.6, 17.067 kS/s, continuing down to about 1.652 kS/s |
| Input range | ±5 V |
| Coupling | Software-selectable AC/DC; IEPE excitation with AC coupling |
| IEPE excitation | 2.0 mA minimum, 2.1 mA typical; 19 V maximum compliance |
| Passband / alias-free bandwidth | 0.45 × sampling rate |
| Stopband | Starts at 0.55 × sampling rate; 100 dB rejection |

Source: [NI-9234 Datasheet](https://download.ni.com/support/manuals/374238a_02.pdf), pp. 1, 5–10.

## NI cDAQ-9171

Verified from the NI cDAQ-9171 Specifications:

| Item | Verified specification |
|---|---|
| Chassis | One-slot, bus-powered USB CompactDAQ chassis |
| USB | USB 2.0 Hi-Speed |
| Maximum analog-input sample rate | Determined by installed C Series module |
| Supported analog-input channels | Determined by installed C Series module |
| Timing accuracy | 50 ppm of sample rate, excluding module group delay |
| Timing resolution | 12.5 ns |

With one NI-9234 installed, the module—not the chassis—sets the four-channel sampling ceiling.

Source: [NI cDAQ-9171 Specifications](https://download.ni.com/support/manuals/374037b.pdf), pp. 1, 4.

## HS Sensors 13A131 accelerometer

The following values are **supplier specifications** and require confirmation against the delivered datasheet and calibration certificate:

| Item | Supplier-listed specification |
|---|---|
| Sensor type | IEPE, uniaxial accelerometer |
| Sensitivity | 100 mV/g |
| Measurement range | ±50 g peak |
| Frequency range | 0.5–10,000 Hz |
| Resonant frequency | ≥25 kHz |
| Broadband resolution | 0.0005 g RMS |
| Excitation voltage | 18–28 VDC |
| Constant-current excitation | 2–10 mA |
| Output bias voltage | 9.5–12.5 VDC |
| Connector | M5 coaxial jack, top entry |
| Mounting thread | M5 |
| Mass | 14.5 g |

Source: [Korea SI product specification page](https://hankooksi.blogspot.com/2024/01/13a131.html), accessed 2026-07-16. This is not yet treated as a manufacturer-primary source.

## Preliminary compatibility assessment

- **Channel count:** four 13A131 sensors can occupy all four NI-9234 input channels, and NI specifies simultaneous sampling for those channels.
- **IEPE current:** the sensor supplier specifies 2–10 mA and NI specifies at least 2.0 mA, typically 2.1 mA. This overlaps at the lower end and is provisionally compatible.
- **Voltage headroom:** at 100 mV/g and ±50 g, nominal sensor output span is ±5 V, equal to the NI-9234 input range. Using the supplier bias range (9.5–12.5 V), the NI compliance check remains nominally within 0–19 V (`bias ± 5 V` gives 4.5–17.5 V). This is an inference and must be confirmed under the actual sensor/cable configuration.
- **Connectors/cables:** the sensor uses an M5 coaxial connection while NI-9234 variants commonly use BNC inputs. Exact purchased NI-9234 connector variant and four compatible low-noise cables/adapters must be checked physically.
- **Grounding and IEPE health:** chassis grounding, bias-voltage checks, cable strain relief, and per-channel noise-floor tests are required during pilot commissioning.

This assessment does not replace the delivered manuals, calibration certificates, or a four-channel bench test.

## Sampling-rate implications — not a final decision

The NI-9234 does not accept every arbitrary rate when using its internal 13.1072 MHz timebase; it uses discrete divided rates. Its alias-free bandwidth is approximately `0.45 × fs`.

| Candidate native rate | NI alias-free bandwidth | Relation to supplier-listed 10 kHz sensor range |
|---:|---:|---|
| 17.067 kS/s | about 7.68 kHz | Does not cover the entire listed sensor range |
| 25.6 kS/s | 11.52 kHz | Covers the listed 10 kHz range nominally |
| 51.2 kS/s | 23.04 kHz | Exceeds the listed calibrated sensor range; increases storage without establishing additional reliable sensor bandwidth |

Therefore, **25.6 kS/s is a hardware-supported candidate** if the study requires the full supplier-listed 0.5–10 kHz sensor range. It is not yet the selected UOS v2 sampling rate. A lower rate may be sufficient if survey evidence and pilot spectra establish a lower diagnostic bandwidth; 51.2 kS/s may be justified for anti-aliasing margin, transient inspection, or later downsampling, but this must be demonstrated.

## Decisions still open

- Final sensor positions, directions, mounting adapters, and cable routing
- Final sampling rate and whether raw acquisition is stored at a higher rate before controlled downsampling
- RPM grid, transient-speed conditions, and tachometer/encoder synchronization
- Record duration, repetitions, segmentation, and total dataset size
- Required diagnostic bandwidth based on rotational frequency, bearing characteristic frequencies, harmonics, sidebands, and envelope spectra
- Whether ±50 g / ±5 V leaves sufficient headroom under severe compound-fault impacts

## Required pilot checks

1. Confirm exact NI-9234 part number/connector and inspect all four signal cables.
2. Archive the delivered 13A131 datasheet and each sensor calibration certificate outside Git; record relative paths in a future equipment-source index.
3. Verify IEPE bias voltage and noise floor on all four channels at rest.
4. Run a common-input or co-located-sensor test to verify gain/phase consistency and channel alignment.
5. Compare candidate locations using fault-frequency/envelope visibility, SNR, repeatability, clipping margin, and channel complementarity.
6. Inspect spectra at candidate rates and choose bandwidth before fixing sampling rate.
7. Estimate storage for four channels across candidate rates and record durations.
