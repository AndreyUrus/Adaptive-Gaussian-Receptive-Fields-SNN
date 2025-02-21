// IJCNN25.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>

#include "../helpers/DatTab/DatTab.h"
#include "../sg/sg.h"

using namespace std;

int main(int ARGC, char *ARGV[])
{
    if (ARGV[1][0] == 'p') {
        DatTab dt("ping_pong_state.labelled.csv", 5);
        VECTOR<PAIR<float, VECTOR<double> > > vprvd_ReceptiveFieldCenters;
        vector<int> vn_{ 5, 10, 5, 10, 10 };
        DatTab dtACRF(dt, vn_, 10, vprvd_ReceptiveFieldCenters);
        dtACRF.store("ping_pong_state.ACRF.labelled.csv");
        FORI(dt.NAtts()) {
            float rmin = *min_element(dt.prGetPredictor(_i), dt.prGetPredictor(_i) + dt.NRecs());
            float rmax = *max_element(dt.prGetPredictor(_i), dt.prGetPredictor(_i) + dt.NRecs());
            vprvd_ReceptiveFieldCenters[_i].first = (rmax - rmin) / (vn_[_i] - 1);
            vprvd_ReceptiveFieldCenters[_i].second.resize(vn_[_i]);
            for (int i = 0; i < vn_[_i]; ++i)
                vprvd_ReceptiveFieldCenters[_i].second[i] = rmin + i * vprvd_ReceptiveFieldCenters[_i].first;
            vprvd_ReceptiveFieldCenters[_i].first *= DEFAULT_RELATIVE_GAUSSIAN_RECEPTIVE_FIELD_WIDTH;
        }
        DatTab dtold(dt, vprvd_ReceptiveFieldCenters, 10);
        dtold.store("ping_pong_state.old.labelled.csv");
    } else {
        DatTab dt("covtype\\covtype.data", 54);
        VECTOR<PAIR<float, VECTOR<double> > > vprvd_ReceptiveFieldCenters;
        DatTab dtACRF(dt, 10, 10, vprvd_ReceptiveFieldCenters);
        dtACRF.store("covtype.ACRF.csv");
        FORI(dt.NAtts()) {
            if (_i < 10) {
                float rmin = *min_element(dt.prGetPredictor(_i), dt.prGetPredictor(_i) + dt.NRecs());
                float rmax = *max_element(dt.prGetPredictor(_i), dt.prGetPredictor(_i) + dt.NRecs());
                vprvd_ReceptiveFieldCenters[_i].first = (rmax - rmin) / 9;
                vprvd_ReceptiveFieldCenters[_i].second.resize(10);
                for (int i = 0; i < 10; ++i)
                    vprvd_ReceptiveFieldCenters[_i].second[i] = rmin + i * vprvd_ReceptiveFieldCenters[_i].first;
                vprvd_ReceptiveFieldCenters[_i].first *= DEFAULT_RELATIVE_GAUSSIAN_RECEPTIVE_FIELD_WIDTH;
            } else vprvd_ReceptiveFieldCenters[_i].second.clear();
        }
        DatTab dtold(dt, vprvd_ReceptiveFieldCenters, 10);
        dtold.store("covtype.old.csv");
    }
	return 0;
}
