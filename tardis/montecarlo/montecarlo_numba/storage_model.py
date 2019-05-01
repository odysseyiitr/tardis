from numba import int64, float64
from astropy import constants as const
storage_model_spec = [
    ('packet_nus', float64[:]),
    ('packet_mus', float64[:]),
    ('packet_energies', float64[:]),
    ('output_nus', float64[:]),
    ('output_energies', float64[:]),
    ('no_of_packets', int64),
    ('no_of_shells', int64),
    ('r_inner', float64[:]),
    ('r_outer', float64[:]),
    ('v_inner', float64[:]),
    ('time_explosion', float64),
    ('inverse_time_explosion', float64),
    ('electron_densities', float64[:]),
    ('inverse_electron_densities', float64[:]), # Maybe remove the inverse things
    ('line_list_nu', float64[:]),
    ('line_lists_tau_sobolevs', float64[:]),
    ('no_of_lines', int64),
    ('line_interaction_id', int64),
#    ('*js', float64),
#    ('*nubars', float64),
    ('sigma_thomson', float64),
    ('inverse_sigma_thomson', float64),
]

class StorageModel(object):
    def __init__(self, packet_nus, packet_mus, packet_energies, 
    output_nus, output_energies, no_of_packets, no_of_shells, 
    r_inner, r_outer, v_inner, time_explosion, electron_densities, line_list_nu, line_lists_tau_sobolevs, 
    no_of_lines, no_of_edges, line_interaction_id, 
    inverse_sigma_thomson):
        self.packet_nus = packet_nus
        self.packet_mus = packet_mus
        self.packet_energies = packet_energies
        self.output_nus = output_nus
        self.output_energies = output_energies
        self.r_inner = r_inner
        self.r_outer = r_outer
        self.v_inner = v_inner
        
        self.time_explosion = time_explosion
        self.inverse_time_explosion = 1 / time_explosion

        self.electron_densities = electron_densities

        self.inverse_electron_densities = 1 / electron_densities
        
        self.sigma_thomson = const.sigma_T.to('cm^2').value
        self.inverse_sigma_thomson = 1 / self.sigma_thomson

def initialize_storage_model(model, plasma, runner):
    storage_model_kwargs = {'packet_nus': runner.input_nu,
    'packet_mus': runner.input_mu,
    'packet_energies': runner.input_energy,
    'output_nus': _output_nu,
    'output_energies': _output_energy,
    'no_of_packets': runner.input_nu.size,
    'no_of_shells': model.no_of_shells,
    'r_inner': runner.r_inner_cgs,
    'r_outer': runner.r_outer_cgs,
    'v_inner': runner.v_inner_cgs,
    'time_explosion': model.time_explosion.to('s').value,
    'electron_densities': plasma.electron_densities.values,
    'line_list_nu': plasma.atomic_data.lines.nu.values,
    'line_lists_tau_sobolevs': runner.line_lists_tau_sobolevs,
    'no_of_lines': plasma.atomic_data.lines.nu.values.size,
    'line_interaction_id': runner.get_line_interaction_id(
        runner.line_interaction_type),
    'inverse_sigma_thomson': 1.0 / storage.sigma_thomson}

    return StorageModel(**storage_model_kwargs))