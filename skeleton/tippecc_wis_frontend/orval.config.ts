module.exports = {
	climateindices: {
		output: {
			mode: 'tags-split',
			target: 'src/schema.ts',
			baseUrl: 'http://127.0.0.1:8000',
			schemas: 'src/model',
			client: 'svelte-query',
			mock: false
		},
		input: {
			target: '../../django/schema.yml'
		}
	}
};
