
{
TLegend *leg = new TLegend(0.48,0.7,0.99,0.9);
TH1F *comparison;

TFile* file10 = new TFile("./out_data_10/outcome.root");
TH1F* tot_vs_th_10 = (TH1F*)file10->Get("tot_vs_th92");

TFile* file15 = new TFile("./out_data_15/outcome.root");
TH1F* tot_vs_th_15 = (TH1F*)file15->Get("tot_vs_th92");


TFile* file20 = new TFile("./out_data_20/outcome.root");
TH1F* tot_vs_th_20 = (TH1F*)file20->Get("tot_vs_th92");


TFile* file35 = new TFile("./out_data_35/outcome.root"); 
TH1F* tot_vs_th_35 = (TH1F*)file35->Get("tot_vs_th92");



tot_vs_th_35->SetLineColor(4);
tot_vs_th_20->SetLineColor(3);
tot_vs_th_15->SetLineColor(2);
tot_vs_th_10->SetLineColor(1);

//comparison = tot_vs_th_10;
//comparison->Draw();
tot_vs_th_35->Draw("e");
tot_vs_th_20->Draw("same e");
tot_vs_th_15->Draw("same e");
tot_vs_th_10->Draw("same e");
leg->AddEntry(tot_vs_th_35,"Peaking time 35 ns","lpf");
leg->AddEntry(tot_vs_th_20,"Peaking time 20 ns","lpf");
leg->AddEntry(tot_vs_th_15,"Peaking time 15 ns","lpf");
leg->AddEntry(tot_vs_th_10,"Peaking time 10 ns","lpf");
leg->Draw();


tot_vs_th_35->GetXaxis()->SetTitle("Threshold [mV]");
tot_vs_th_35->GetYaxis()->SetTitle("Time over threshold [ns]");

}
