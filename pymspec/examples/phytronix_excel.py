# -*- coding: utf8 -*-

__author__ = 'Alexandre Drouin'

raise RuntimeError("This example is deprecated and must be updated.")

import numpy as np
from pymspec.io.excel.file import PhytronixExcelFile
from pymspec.spectrum import Spectrum
from pymspec.preprocessing.raw import BackgroundPeakRemoval, IntensityValueNormalization
from pymspec.visualization.plot import SpectrumPlot

#XXX: DELETE ME LATER OR MERGE ME
from pymspec.preprocessing.raw import PreprocessorMixin
class NegativePeakRemover(PreprocessorMixin):
    def __init__(self):
        pass

    def __call__(self, peaks):
        mz_values = np.array(peaks.keys())
        intensity_values = np.array(peaks.values())

        new_intensity_values = intensity_values[intensity_values >= 0.0]
        new_mz_values = mz_values[intensity_values >= 0.0]

        return dict(zip(new_mz_values, new_intensity_values))

    def __str__(self):
        return "NegativePeakRemover()"


file = PhytronixExcelFile("/Users/Alexandre/Google Drive/Données CHUL/2013-12-19/20131219002_Scan pos test.xlsx")

# Charge les spectres moyens pour chaque échantillon (water et patients)
# On fixe les peaks d'intensité négative à 0 et on les enlève
# On normalise les spectres selon leur norme (Reste à déterminer si c'est une bonne idée on
# peut aussi normaliser par rapport à la somme totale des intensités ou au peak d'intensité maximum)
mean_spectra = file.get_mean_spectra(mz_precision=2, preprocessing_steps=[NegativePeakRemover(), IntensityValueNormalization()])

# Étant donné les spectres moyens des patients, on affiche leur superposition.
all_patient_mean = SpectrumPlot(title="Patient mean spectra", spectra=mean_spectra, spectra_labels=["Patient " + s.metadata["sample_name"] for s in mean_spectra], show_spectra=True, x_label="m/z", y_label="Intensity")
all_patient_mean.show()


# Obtenir un spectre de patient malade en fonction de son numéro
patient_malade = [x for x in mean_spectra if x.metadata["sample_name"] == u'679480856'][0]
# Obtenir un spectre de patient sain en fonction de son numéro
patient_sain = [x for x in mean_spectra if x.metadata["sample_name"] == u'3004840760'][0]

# Exemple de soustraction de spectres. On génère un nouveau spectre en donnant BackgroundPeakRemoval comme preprocessing step
# Éventuellement on pourra implémenter la soustraction de spectres mais je ne voulais pas perdre de temps à essayer de matcher
# les valeurs de mz
diff = Spectrum(mz_values=patient_sain.mz_values(), mz_precision=patient_sain.mz_precision, intensity_values=patient_sain.intensity_values(), metadata=patient_sain.metadata, preprocessing_steps=[BackgroundPeakRemoval(patient_malade)])
# Un spectrum plot sert à afficher un spot d'une liste de spectres (Voir classe pour paramètres)
SpectrumPlot(spectra=[diff], spectra_labels=["sain-malade"]).show()

# Charge tous les spectres pour chaque échantillon (sous la forme d'une liste de listes)
# On fixe les peaks d'intensité négative à 0 et on les enlève
# On normalise les spectres selon leur norme (Reste à déterminer si c'est une bonne idée on
# peut aussi normaliser par rapport à la somme totale des intensités ou au peak d'intensité maximum)
spectra = file.get_spectra(mz_precision=2, preprocessing_steps=[NegativePeakRemover(), IntensityValueNormalization()])

# Pour les différents scans d'un même patient
for patient in xrange(len(spectra)):
    sample_name = spectra[patient][0].metadata["sample_name"]

    # Dany: Ici tu pourrais comprendre à quoi servent les différents paramètres de la classe. Je les utilise tous.

    mean_no_uncertainty = SpectrumPlot(title="Patient "+ sample_name, spectra=spectra[patient], spectra_labels=["scan"+str(i+1) for i in xrange(len(spectra[patient]))], x_label="m/z", y_label="Intensity", show_spectra=False, show_mean_spectrum=True, show_uncertainty=False)
    mean_no_uncertainty.show()

    mean_with_uncertainty = SpectrumPlot(title="Patient "+ sample_name, spectra=spectra[patient], spectra_labels=["scan"+str(i+1) for i in xrange(len(spectra[patient]))], x_label="m/z", y_label="Intensity", show_spectra=False, show_mean_spectrum=True, show_uncertainty=True)
    mean_with_uncertainty.show()

    all_spectra = SpectrumPlot(title="Patient "+ sample_name, spectra=spectra[patient], spectra_labels=["scan"+str(i+1) for i in xrange(len(spectra[patient]))], x_label="m/z", y_label="Intensity", show_spectra=True, show_mean_spectrum=False, show_uncertainty=False)
    all_spectra.show()

    all_spectra_with_mean_no_uncertainty = SpectrumPlot(title="Patient "+ sample_name, spectra=spectra[patient], spectra_labels=["scan"+str(i+1) for i in xrange(len(spectra[patient]))], x_label="m/z", y_label="Intensity", show_spectra=True, show_mean_spectrum=True, show_uncertainty=False)
    all_spectra_with_mean_no_uncertainty.show()
