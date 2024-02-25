module.exports = {
	climateindices: {
		output: {
			mode: 'tags-split',
			target: 'src/schema.ts',
			baseUrl: 'https://leutra.geogr.uni-jena.de/backend_geoportal_fabian',
			schemas: 'src/model',
			client: 'svelte-query',
			mock: false
		},
		input: {
			target: '../../django/schema.yml'
		}
	}
};
