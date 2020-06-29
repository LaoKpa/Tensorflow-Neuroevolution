class CoDeepNEATSpeciationMOD:
    def _speciate_modules_basic(self, new_module_ids):
        """"""
        # Determine module type of each species before all members of the species are
        species_mod_type_to_id = dict()
        for spec_id, spec_mod_ids in self.mod_species.items():
            spec_mod_type = self.modules[spec_mod_ids[0]].get_module_type()
            species_mod_type_to_id[spec_mod_type] = spec_id

        ### Removal of parental but not elite Modules ###
        # Remove modules that will not be carried over from module container after evolution, though which were kept as
        # potential parent
        for spec_id, spec_mod_ids in self.mod_species.items():
            # Sort module ids in species according to their fitness
            spec_mod_ids_sorted = sorted(spec_mod_ids, key=lambda x: self.modules[x].get_fitness(), reverse=True)

            # Determine module ids that were kept but are not carried over
            spec_mod_ids_to_carry_over = spec_mod_ids_sorted[:self.mod_spec_mod_elitism]
            spec_mod_ids_to_remove = [mod_id for mod_id in spec_mod_ids if mod_id not in spec_mod_ids_to_carry_over]

            # Delete just determined module ids from module container and module species list
            for mod_id_to_remove in spec_mod_ids_to_remove:
                self.mod_species[spec_id].remove(mod_id_to_remove)
                del self.modules[mod_id_to_remove]

        ### Species Assignment ###
        # Basic speciation assigns each new module to the species with the according module type, as for each module
        # type there is only one species
        for mod_id in new_module_ids:
            mod_type = self.modules[mod_id].get_module_type()
            according_mod_spec_id = species_mod_type_to_id[mod_type]
            self.mod_species[according_mod_spec_id].append(mod_id)