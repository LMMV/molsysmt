# =======================
# Potential Energy
# =======================

"""
Potential Energy
================

Methods related with the potential energy of the system.
From energy minimization to potential energy contribution of specific set of atoms or interactions.
"""

from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest()
def get_potential_energy(molecular_system, selection='all', decomposition=False, platform='CPU',
        engine='OpenMM', syntax='MolSysMT', skip_digestion=False):

    from molsysmt import convert, get_form, has_attribute
    from molsysmt.config import default_attribute

    if engine=='OpenMM':

        import openmm as mm

        form_in = get_form(molecular_system)

        if form_in == 'openmm.Context':

            if is_all(selection):

                context=molecular_system

            else:

                from molsysmt.form.openmm_Context import extract

                context=extract(molecular_system, selection=selection, syntax=syntax)

        elif form_in == 'openmm.Simulation':

            if is_all(selection):

                context = item.context

            else:

                from molsysmt.form.openmm_Simulation import extract

                context=extract(molecular_system, selection=selection, syntax=syntax)

        else:

            extra_conversion_arguments={}

            possible_missing_attributes=['forcefield', 'water_model', 'implicit_solvent', 'constraints',
                    'non_bonded_method', 'switch_distance', 'dispersion_correction', 'ewald_error_tolerance',
                    'integrator', 'temperature', 'friction', 'time_step']

            for att in possible_missing_attributes:
                if not has_attribute(molecular_system, att):
                    extra_conversion_arguments[att]=default_attribute[att]

            context = convert(molecular_system, to_form='openmm.Context', selection=selection,
                    syntax=syntax, **extra_conversion_arguments, platform=platform)

        if decomposition:

            tmp_system = context.getSystem()

            forcegroups = {}
            for ii in range(tmp_system.getNumForces()):
                force = tmp_system.getForce(ii)
                force.setForceGroup(ii)
                forcegroups[force] = ii

            tmp_context = mm.Context(tmp_system, mm.VerletIntegrator(0.001), context.getPlatform())
            tmp_context.setPositions(context.getState(getPositions=True).getPositions())

            context_forcegroups = {}
            for forcegroup, ii in forcegroups.items():
                context_forcegroups[forcegroup.getName()] = tmp_context.getState(getEnergy=True, groups={ii})

            output = {}
            for forcegroup_name, tmp_context in context_forcegroups.items():
                output[forcegroup_name] = tmp_context.getPotentialEnergy()

            for energy_term, energy_value in output.items():
                output[energy_term]=puw.standardize(energy_value)

        else:

            state = context.getState(getEnergy=True)
            output = state.getPotentialEnergy()
            output = puw.standardize(output)

        return output

    else:

        raise NotImplementedError

