import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np
import scipy as sp
from warnings import filterwarnings
filterwarnings(action='ignore')

save_image = True


def m_bps(t):
    f16 = np.cos(32 * np.pi * t) - np.sin(32 * np.pi * t)
    f18 = -np.cos(36 * np.pi * t) - np.sin(36 * np.pi * t)
    f22 = np.cos(44 * np.pi * t) + np.sin(44 * np.pi * t)
    f24 = -np.cos(48 * np.pi * t) - np.sin(48 * np.pi * t)
    return f16 + f18 + f24 + f22


def m_real(t):
    return 2 * np.sin(4 * np.pi * t)


def m_imag(t):
    return 2 * (np.sin(4 * np.pi * t) - np.sin(8 * np.pi * t) + np.cos(8 * np.pi * t))


def a(t):
    return m_real(t) * np.cos(40 * np.pi * t)


def b(t):
    return m_imag(t) * np.sin(40 * np.pi * t)


def find_duty():
    for T in np.arange(.25, 40, .125):
        duty1, _ = sp.integrate.quad(lambda x: m_bps(x), 0, T)
        duty2, _ = sp.integrate.quad(lambda x: m_bps(x), T, 2 * T)

        if abs(duty2 - duty1) < 1e-15:
            return T

# Prepare sample setting.
sample_rate = 1000  # number of unit per second.
total_second = 2
total_point = sample_rate * total_second

# Produce time-series and all signal in time-domain.
time = np.linspace(0, total_second, total_point)
amplitude = m_bps(time)
mI = m_real(time)
mQ = m_imag(time)
r = np.sqrt(mI ** 2 + mQ ** 2)
a_ = a(time)
b_ = b(time)
c_ = a_ - b_
duty = find_duty()


#  Do Fourier Transform on Bandpass Signal
Fm_intensity_complex = sp.fft.fft(amplitude, n=int(sample_rate * duty))  # Is a list of complex number
Fm_freq = sp.fft.fftfreq(Fm_intensity_complex.shape[0], 1 / sample_rate)
#  Fm_freq = Fm_freq[:len(Fm_freq) // 2]
Fm_intensity_square = np.abs(Fm_intensity_complex)  # Do abs let the complex number go to the real number.

#  Cut out the negative part
Fm_freq_p = Fm_freq[Fm_freq >= 0]
Fm_intensity_square_p = Fm_intensity_square[Fm_freq >= 0]

#  Make shifted major spectrum.
major_freq = Fm_freq_p[np.argwhere(Fm_intensity_square_p >= Fm_intensity_square_p.max() * .95)]
shifted_spec = major_freq - major_freq.mean()

#  Make baseband equivalent signal spectrum.
Fm_prime_freq = Fm_freq_p - major_freq.mean()
Fm_prime_intensity = 2 * Fm_intensity_square_p



#  Plotting m(t) signal.
#  For question 1
plt.figure(figsize=(15, 6))
plt.plot(time, amplitude)
plt.ylabel('$m(t)$', fontsize=25)
plt.xlabel('Time(sec)', fontsize=25)
plt.vlines(0, amplitude.min(), amplitude.max(), 'black')
plt.hlines(0, time.min(), time.max(), 'black')
plt.grid()
plt.legend()

if save_image:
    plt.savefig(f'./image/h1/Q1.png')
    plt.close()
else:
    plt.show()

# Plotting M'(t), the spectrum of m'(t)
# For question 4
plt.figure(figsize=(15, 6))
# plt.stem(Fm_freq_p[Fm_freq_p <= 100] - major_freq.mean(), Fm_real_p[Fm_freq_p <= 100])
plt.stem(
    Fm_prime_freq[Fm_prime_freq <= 24],
    Fm_prime_intensity[Fm_prime_freq <= 24] / Fm_intensity_square.max())
plt.xticks(np.arange(-24, 24, 2))
plt.xlabel('Frequency(Hz)')
plt.ylabel('$\\frac{|M^\prime|}{|M|}$', rotation=0)
plt.grid()

if save_image:
    plt.savefig(f'./image/h1/Q4.png')
    plt.close()
else:
    plt.show()



#  Plotting mI(t), mQ(t) and r(t)
#  For question 7
plt.figure(figsize=(15, 10), dpi=72)
plt.plot(time, mI, label='$m_I(t)$')
plt.plot(time, mQ, label='$m_Q(t)$')
plt.plot(time, r, label='$r(t)$')
plt.legend(fontsize=25)
plt.xlabel('Time(sec)', fontsize=25)
plt.ylabel('Intensity', fontsize=25)
plt.vlines(0, mQ.min(), r.max(), 'black')
plt.hlines(0, time.min(), time.max(), 'black')
plt.grid()
if save_image:
    plt.savefig(f'./image/h1/Q7.png')
    plt.close()
else:
    plt.show()

#  Plotting m(t) and complex envelop
#  For question 8
plt.figure(figsize=(15, 10), dpi=72)
plt.plot(time, m_bps(time), label=f'$m(t)$')
plt.plot(time, r, 'r:', linewidth=3, label='Complex Envelope: $\pm r(t)$')
plt.plot(time, -r, 'r:', linewidth=3)
plt.ylabel(f'Intensity', fontsize=25)
plt.xlabel(f'Time(sec)', fontsize=25)
plt.grid()
plt.vlines(0, -r.min(), r.max(), 'black')
plt.hlines(0, time.min(), time.max(), 'black')
plt.legend(fontsize=25)
if save_image:
    plt.savefig(f'./image/h1/Q8.png')
    plt.close()
else:
    plt.show()

#  Plotting signal of c(t) = m_I(t) * sin(2pi20t) - m_Q(t) * cos(2pi20t)
#  For question 9
pfg = plt.figure(figsize=(15, 10), dpi=72)
ax1 = pfg.add_subplot(2, 1 ,1)
ax2 = pfg.add_subplot(2, 1 ,2)

ax1.plot(time, c_, label='$c(t)$')
ax1.grid()
ax1.set_xlabel('Time(sec)', fontsize=25)
ax1.set_ylabel('Intensity', fontsize=25)
ax1.legend(fontsize=25)

ax2.plot(time, amplitude, label='$m(t)$')
ax2.grid()
ax2.set_xlabel('Time(sec)', fontsize=25)
ax2.set_ylabel('Intensity', fontsize=25)
# ax2.set_ylim([-5, 5])
ax2.legend(fontsize=25)

for single_d in np.arange(0, time.max(), duty):
    ax1.axvline(x=single_d, ymin=-1, ymax=1,c="red",linewidth=2,zorder=0, clip_on=False)
    ax2.axvline(x=single_d, ymin=0, ymax=1,c="red",linewidth=2,zorder=0, clip_on=False)

plt.draw()

if save_image:
    plt.savefig(f'./image/h1/Q9.png')
    plt.close()
else:
    plt.show()