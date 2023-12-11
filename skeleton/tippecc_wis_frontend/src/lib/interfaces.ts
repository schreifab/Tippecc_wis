export interface Dataset {
    name: string;
    desc: string;
    filter_word: string;
    optional: boolean;
}

export interface Parameter {
    name: string;
    desc: string;
    input_list: string[];
    unit_list: string[];
    datatype: string;
    optional: boolean;
}

export interface FunctionDetails {
    id: number
    datasets: Dataset[];
    parameters: Parameter[];
}