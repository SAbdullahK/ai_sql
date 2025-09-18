import React, { useState } from "react";
import { MdPlayArrow, MdBarChart, MdDashboard } from "react-icons/md";
import { IoMdHome } from "react-icons/io";
import { IoDocuments } from "react-icons/io5";

import Card from "components/card";
import Widget from "components/widget/Widget";

const Dashboard = () => {
  const [userQuery, setUserQuery] = useState("");
  const [answer, setAnswer] = useState("");   // final natural language answer

  const handleGenerate = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userQuery }),
      });

      const data = await response.json();
      console.log("Backend response:", data);

      // ✅ Flask currently returns only "answer"
      setAnswer(data.answer || "");
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <div>
      {/* === Top Stats Boxes === */}
      <div className="mt-3 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-3 3xl:grid-cols-6">
        <Widget icon={<MdBarChart className="h-7 w-7" />} title={"Earnings"} subtitle={"$340.5"} />
        <Widget icon={<IoDocuments className="h-6 w-6" />} title={"Spend this month"} subtitle={"$642.39"} />
        <Widget icon={<MdBarChart className="h-7 w-7" />} title={"Sales"} subtitle={"$574.34"} />
        <Widget icon={<MdDashboard className="h-6 w-6" />} title={"Your Balance"} subtitle={"$1,000"} />
        <Widget icon={<MdBarChart className="h-7 w-7" />} title={"New Tasks"} subtitle={"145"} />
        <Widget icon={<IoMdHome className="h-6 w-6" />} title={"Total Projects"} subtitle={"$2433"} />
      </div>

      {/* === SQL Query Generator Section === */}
      <Card extra="mt-5 p-6">
        <h2 className="text-xl font-bold text-navy-700 dark:text-white mb-4">
          SQL Query Generator
        </h2>

        {/* Input field */}
        <textarea
          value={userQuery}
          onChange={(e) => setUserQuery(e.target.value)}
          placeholder="Ask me anything about your database (e.g. 'Show all employees in HR')"
          className="w-full p-3 rounded-lg border border-gray-300 dark:border-navy-600 dark:bg-navy-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-500"
          rows={3}
        />

        {/* Generate button */}
        <button
          onClick={handleGenerate}
          className="mt-4 flex items-center justify-center gap-2 rounded-lg bg-brand-500 px-4 py-2 text-white font-semibold hover:bg-brand-600 transition"
        >
          <MdPlayArrow className="h-5 w-5" />
          Generate SQL
        </button>

        {/* Natural Language Answer */}
        {answer && (
          <div className="mt-5 p-4 rounded-lg bg-green-100 dark:bg-navy-700">
            <strong>Answer:</strong>
            <p className="mt-1 text-gray-800 dark:text-white">{answer}</p>
          </div>
        )}
      </Card>
    </div>
  );
};

export default Dashboard;
